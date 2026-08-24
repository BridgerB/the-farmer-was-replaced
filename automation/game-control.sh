#!/usr/bin/env bash
# Sends game-control keystrokes into the private automation compositor via
# xdotool/XTEST (see launch-game.sh / flake.nix for why XTEST rather than
# Wayland-protocol injection). Mirrors the start|stop|status interface of
# the Windows game_control.ahk script, including the OK:/ERROR: stdout
# convention the MCP server's control layer checks for.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

ACTION="${1:-start}"

if [ ! -f "$FARMER_ENV_FILE" ]; then
	echo "ERROR: automation environment not up (run start-env.sh)"
	exit 1
fi
set -a
source "$FARMER_ENV_FILE"
set +a

window_present() {
	xdotool search --name "TheFarmerWasReplaced" >/dev/null 2>&1
}

case "$ACTION" in
status)
	if window_present; then
		echo "OK: Game running"
	else
		echo "ERROR: Game not found"
		exit 1
	fi
	;;
start)
	window_present || {
		echo "ERROR: Game not found"
		exit 1
	}
	xdotool key F5
	echo "OK: Started"
	;;
stop)
	window_present || {
		echo "ERROR: Game not found"
		exit 1
	}
	xdotool key shift+F5
	echo "OK: Stopped"
	;;
*)
	echo "ERROR: unknown action '$ACTION' (expected start|stop|status)"
	exit 1
	;;
esac
