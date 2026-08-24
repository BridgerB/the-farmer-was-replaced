#!/usr/bin/env bash
# Opens a live, interactive view of the private automation compositor as a
# normal window on your REAL desktop: wayvnc serves the private compositor
# over VNC (loopback-only), wlvncc connects to it and renders as a native
# Wayland window on your actual session - mouse/keyboard you use in that
# window get forwarded over VNC into the private compositor, they never
# touch your real desktop's other windows or the private compositor's
# libinput/uinput layer (there isn't one - see start-env.sh).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

if [ ! -f "$FARMER_ENV_FILE" ]; then
	echo "automation environment not up - run start-env.sh first" >&2
	exit 1
fi

REAL_WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-}"
if [ -z "$REAL_WAYLAND_DISPLAY" ]; then
	echo "no WAYLAND_DISPLAY in this shell - run view.sh from a terminal on your real desktop" >&2
	exit 1
fi

PORT="${FARMER_VNC_PORT:-5951}"

if pid_running "$FARMER_WAYVNC_PID_FILE"; then
	echo "wayvnc already running on 127.0.0.1:$PORT"
else
	# wayvnc targets whatever WAYLAND_DISPLAY/SWAYSOCK are in ITS env - the
	# private compositor's, from the env file sourced below.
	(
		set -a
		source "$FARMER_ENV_FILE"
		set +a
		exec wayvnc --render-cursor --socket="$FARMER_STATE_DIR/wayvnc-ctl.sock" 127.0.0.1 "$PORT"
	) >"$FARMER_WAYVNC_LOG" 2>&1 &
	echo $! >"$FARMER_WAYVNC_PID_FILE"
	sleep 1
	if ! kill -0 "$(cat "$FARMER_WAYVNC_PID_FILE")" 2>/dev/null; then
		echo "FAILED: wayvnc exited immediately, see $FARMER_WAYVNC_LOG" >&2
		cat "$FARMER_WAYVNC_LOG" >&2
		rm -f "$FARMER_WAYVNC_PID_FILE"
		exit 1
	fi
	echo "wayvnc up on 127.0.0.1:$PORT (private compositor)"
fi

echo "opening viewer window on your real desktop..."
WAYLAND_DISPLAY="$REAL_WAYLAND_DISPLAY" wlvncc --app-id=farmer-viewer 127.0.0.1 "$PORT"
