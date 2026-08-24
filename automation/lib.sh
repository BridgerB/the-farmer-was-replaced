# Shared state for the automation scripts. Sourced, not executed directly.

FARMER_STATE_DIR="${XDG_RUNTIME_DIR:-/tmp}/farmer-automation"
mkdir -p "$FARMER_STATE_DIR"

FARMER_SWAY_PID_FILE="$FARMER_STATE_DIR/sway.pid"
FARMER_SWAY_LOG="$FARMER_STATE_DIR/sway.log"
FARMER_ENV_FILE="$FARMER_STATE_DIR/env"
FARMER_WAYVNC_PID_FILE="$FARMER_STATE_DIR/wayvnc.pid"
FARMER_WAYVNC_LOG="$FARMER_STATE_DIR/wayvnc.log"

pid_running() {
	[ -f "$1" ] && kill -0 "$(cat "$1")" 2>/dev/null
}
