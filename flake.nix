{
  description = "Automation environment for The Farmer Was Replaced: a private headless Sway compositor (its own XWayland, no window on the real desktop) driven via xdotool/XTEST against that private DISPLAY, used to drive the game via the farmer MCP server without touching the real desktop session or its physical input devices.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # steam-run pulls in an unfree package (steam-unwrapped) purely for its
        # FHS sandbox - needed because reaper/pressure-vessel are prebuilt
        # binaries hardcoded to FHS paths like /lib/ld-linux.so.2.
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            nodejs_22
            sway
            xdotool # XTEST-based input injection against the private XWayland DISPLAY.
                    # Tried Wayland-protocol injection first (wtype/wlrctl): pointer motion
                    # reached the game but button/key press state did not reliably register
                    # in testing, so XTEST is the mechanism actually in use.
            wayvnc # VNC server, run against the private compositor's WAYLAND_DISPLAY
            wlvncc # Wayland-native VNC client - shows up as a normal window on the
                   # REAL desktop, forwarding mouse/keyboard into the private compositor
                   # over VNC protocol (see automation/view.sh)
            grim
            slurp
            jq
            wl-clipboard
            steam-run # FHS sandbox reaper/pressure-vessel need (see launch-game.sh)
          ];

          shellHook = ''
            export FARMER_REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
            export PATH="$FARMER_REPO_ROOT/automation:$PATH"
            echo "farmer automation devShell ready."
            echo "  automation/start-env.sh   bring up the private compositor"
            echo "  automation/launch-game.sh launch the game into it"
            echo "  automation/stop-env.sh    tear everything down"
          '';
        };
      });
}
