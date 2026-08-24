#!/usr/bin/env bash
# Tears down the private automation compositor cleanly.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

stop_pid_file() {
	local name="$1" file="$2"
	if pid_running "$file"; then
		local pid
		pid=$(cat "$file")
		echo "stopping $name (pid $pid)..."
		kill "$pid" 2>/dev/null
		for _ in $(seq 1 30); do
			kill -0 "$pid" 2>/dev/null || break
			sleep 0.1
		done
		kill -0 "$pid" 2>/dev/null && kill -9 "$pid" 2>/dev/null
	else
		echo "$name: not running"
	fi
	rm -f "$file"
}

stop_pid_file "wayvnc" "$FARMER_WAYVNC_PID_FILE"
stop_pid_file "sway" "$FARMER_SWAY_PID_FILE"

rm -f "$FARMER_ENV_FILE"
echo "done."
