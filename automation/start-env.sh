#!/usr/bin/env bash
# Brings up the private automation compositor: a Sway instance the real
# Hyprland session never sees. Input is injected purely via Wayland
# protocols (wtype/wlrctl) directly against this compositor's own socket -
# deliberately NOT via ydotool/uinput, which would require this compositor's
# libinput backend to enumerate real input devices and risk grabbing the
# host's physical keyboard/mouse away from the real desktop session.
#
# Mode is chosen by FARMER_COMPOSITOR_MODE:
#   headless (default) - WLR_BACKENDS=headless, fully invisible, no window
#                         appears on the real desktop.
#   nested              - plain `sway` launched as an ordinary Wayland client
#                         of the CURRENT compositor (shows up as one window).
#                         Fallback if headless rendering doesn't work on this
#                         NVIDIA setup.
#
# Idempotent: re-running while already up just reports status and exits 0.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

MODE="${FARMER_COMPOSITOR_MODE:-headless}"

if pid_running "$FARMER_SWAY_PID_FILE" && [ -f "$FARMER_ENV_FILE" ]; then
	echo "already running (mode recorded in $FARMER_ENV_FILE):"
	cat "$FARMER_ENV_FILE"
	exit 0
fi

echo "starting sway (mode=$MODE)..."

RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
MARKER="$FARMER_STATE_DIR/start-marker"
touch "$MARKER"
sleep 0.1 # filesystem mtime resolution margin

if [ "$MODE" = "headless" ]; then
	env \
		WLR_BACKENDS=headless \
		WLR_LIBINPUT_NO_DEVICES=1 \
		WLR_NO_HARDWARE_CURSORS=1 \
		sway -c "$SCRIPT_DIR/sway-headless.conf" \
		>"$FARMER_SWAY_LOG" 2>&1 &
else
	sway -c "$SCRIPT_DIR/sway-headless.conf" >"$FARMER_SWAY_LOG" 2>&1 &
fi
SWAY_PID=$!
echo "$SWAY_PID" >"$FARMER_SWAY_PID_FILE"

# Sway may end up reparented (its launching shell can exit before it does),
# so match by "socket file newer than our marker" rather than by exact PID.
FARMER_WAYLAND_DISPLAY=""
for _ in $(seq 1 50); do
	NEWLOCK=$(find "$RUNTIME_DIR" -maxdepth 1 -name 'wayland-*.lock' -newer "$MARKER" 2>/dev/null | sort | tail -1)
	if [ -n "$NEWLOCK" ]; then
		FARMER_WAYLAND_DISPLAY=$(basename "$NEWLOCK" .lock)
		break
	fi
	sleep 0.1
done

if [ -z "$FARMER_WAYLAND_DISPLAY" ]; then
	echo "  FAILED: could not determine the Wayland display sway chose, see $FARMER_SWAY_LOG" >&2
	cat "$FARMER_SWAY_LOG" >&2
	exit 1
fi
FARMER_SWAYSOCK=""
for _ in $(seq 1 30); do
	FARMER_SWAYSOCK=$(find "$RUNTIME_DIR" -maxdepth 1 -name "sway-ipc.$(id -u).*.sock" -newer "$MARKER" 2>/dev/null | sort | tail -1)
	[ -n "$FARMER_SWAYSOCK" ] && break
	sleep 0.1
done

# The game targets X11 (XWayland) on this system, not native Wayland -
# find the private XWayland socket sway just created for us.
FARMER_DISPLAY=""
for _ in $(seq 1 50); do
	NEWX=$(find /tmp/.X11-unix -maxdepth 1 -name 'X*' -newer "$MARKER" 2>/dev/null | sort | tail -1)
	if [ -n "$NEWX" ]; then
		FARMER_DISPLAY=":$(basename "$NEWX" | sed 's/^X//')"
		break
	fi
	sleep 0.1
done

echo "  sway up: WAYLAND_DISPLAY=$FARMER_WAYLAND_DISPLAY SWAYSOCK=${FARMER_SWAYSOCK:-<not found>} DISPLAY=${FARMER_DISPLAY:-<not found>}"

if [ "$MODE" = "headless" ]; then
	echo "checking headless output exists..."
	OUTPUTS=$(WAYLAND_DISPLAY="$FARMER_WAYLAND_DISPLAY" SWAYSOCK="$FARMER_SWAYSOCK" swaymsg -t get_outputs -r 2>&1)
	if ! echo "$OUTPUTS" | grep -q '"name"'; then
		echo "  no output present, creating one via 'swaymsg create_output'..."
		WAYLAND_DISPLAY="$FARMER_WAYLAND_DISPLAY" SWAYSOCK="$FARMER_SWAYSOCK" swaymsg create_output || true
		sleep 0.3
		OUTPUTS=$(WAYLAND_DISPLAY="$FARMER_WAYLAND_DISPLAY" SWAYSOCK="$FARMER_SWAYSOCK" swaymsg -t get_outputs -r 2>&1)
	fi
	echo "  outputs: $OUTPUTS"
fi

cat >"$FARMER_ENV_FILE" <<EOF
FARMER_COMPOSITOR_MODE=$MODE
WAYLAND_DISPLAY=$FARMER_WAYLAND_DISPLAY
SWAYSOCK=$FARMER_SWAYSOCK
DISPLAY=$FARMER_DISPLAY
EOF

echo
echo "environment up. To use it in another shell:"
echo "  set -a; source $FARMER_ENV_FILE; set +a"
echo
echo "sanity check:"
echo "  WAYLAND_DISPLAY=$FARMER_WAYLAND_DISPLAY SWAYSOCK=$FARMER_SWAYSOCK grim /tmp/farmer-test.png"
