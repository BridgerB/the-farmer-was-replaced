#!/usr/bin/env bash
# Launches The Farmer Was Replaced into the private automation compositor
# (started by start-env.sh), instead of the real desktop.
#
# This replicates the exact command Steam itself uses to launch the game
# (captured from `ps`/`/proc/<pid>/cmdline` of a real Steam-launched session)
# rather than going through Steam's GUI or its (binary, unsafe to hand-edit)
# per-game launch options. Only the display-related env vars are overridden;
# everything else (STEAM_COMPAT_*, XDG_RUNTIME_DIR) is reused as Steam sets it.
#
# reaper/pressure-vessel are prebuilt binaries expecting an FHS filesystem
# (e.g. a hardcoded /lib/ld-linux.so.2 interpreter path), which bare NixOS
# doesn't provide - hence the `steam-run` wrapper below, the same FHS sandbox
# NixOS's steam package itself uses (visible as the `bwrap`/`steam-run-fhs`
# process wrapping a normal Steam launch).
#
# Fragile by nature: hardcodes this install's current paths/Proton version.
# If Steam changes the library layout or updates Proton, re-capture with:
#   pgrep -af "reaper SteamLaunch AppId=2060160"
#   tr '\0' '\n' < /proc/<pid>/cmdline
#   tr '\0' '\n' < /proc/<pid>/environ | grep STEAM_COMPAT
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

if [ ! -f "$FARMER_ENV_FILE" ]; then
	echo "automation environment not up - run start-env.sh first" >&2
	exit 1
fi
set -a
source "$FARMER_ENV_FILE"
set +a

# A plain `pgrep -f "reaper SteamLaunch AppId=2060160"` is unsafe here: it
# substring-matches ANY process's full command line, including unrelated
# shells that merely happen to mention this text (e.g. this very script's
# own comments, quoted in some other shell). Check actual argv[] instead.
already_running() {
	local pid argv0 argv1 argv2
	for pid in /proc/[0-9]*; do
		[ -r "$pid/cmdline" ] || continue
		mapfile -d '' -t argv <"$pid/cmdline" 2>/dev/null || continue
		argv0="${argv[0]:-}"
		argv1="${argv[1]:-}"
		argv2="${argv[2]:-}"
		if [[ "$argv0" == */reaper ]] && [ "$argv1" = "SteamLaunch" ] && [ "$argv2" = "AppId=2060160" ]; then
			return 0
		fi
	done
	return 1
}

if already_running; then
	echo "the game (Steam AppId 2060160) is already running somewhere - refusing to launch a second copy." >&2
	echo "(Steam DRM / save.json integrity do not tolerate concurrent instances.)" >&2
	exit 1
fi

STEAM_ROOT="$HOME/.local/share/Steam"
PROTON="$STEAM_ROOT/steamapps/common/Proton - Experimental"
RUNTIME="/run/media/bridger/6TB/SteamLibrary/steamapps/common/SteamLinuxRuntime_4"
GAME_DIR="$STEAM_ROOT/steamapps/common/The Farmer Was Replaced"
APPID=2060160

exec steam-run env \
	SteamAppId=$APPID \
	SteamGameId=$APPID \
	STEAM_COMPAT_APP_ID=$APPID \
	STEAM_COMPAT_CLIENT_INSTALL_PATH="$STEAM_ROOT" \
	STEAM_COMPAT_DATA_PATH="$STEAM_ROOT/steamapps/compatdata/$APPID" \
	STEAM_COMPAT_INSTALL_PATH="$GAME_DIR" \
	STEAM_COMPAT_SHADER_PATH="$STEAM_ROOT/steamapps/shadercache/$APPID" \
	STEAM_COMPAT_MEDIA_PATH="$STEAM_ROOT/steamapps/shadercache/$APPID/fozmediav1" \
	STEAM_COMPAT_TRANSCODED_MEDIA_PATH="$STEAM_ROOT/steamapps/shadercache/$APPID" \
	STEAM_COMPAT_MOUNTS="$PROTON:$RUNTIME" \
	STEAM_COMPAT_TOOL_PATHS="$PROTON:$RUNTIME" \
	STEAM_COMPAT_LIBRARY_PATHS="$STEAM_ROOT/steamapps:/run/media/bridger/6TB/SteamLibrary/steamapps" \
	STEAM_COMPAT_PROTON=1 \
	STEAM_COMPAT_FLAGS=search-cwd \
	PROTON_CRASH_REPORT_DIR=/tmp/proton_crashreports \
	XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}" \
	WAYLAND_DISPLAY="$WAYLAND_DISPLAY" \
	SWAYSOCK="$SWAYSOCK" \
	DISPLAY="$DISPLAY" \
	"$STEAM_ROOT/ubuntu12_32/reaper" SteamLaunch AppId=$APPID -- \
	"$RUNTIME/_v2-entry-point" --verb=waitforexitandrun -- \
	"$PROTON/proton" waitforexitandrun \
	"$GAME_DIR/TheFarmerWasReplaced.exe"
