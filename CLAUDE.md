# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Automation scripts for "The Farmer Was Replaced" — a Steam game where you write Python-like code to
control drones farming a grid. This repo is the game's **save folder under version control**, plus a
simulation-driven benchmark harness used to optimize each resource's farming strategy.

## Repository Layout

```
Save0/          the actual game save — ALL .py files live here, flat, no subdirectories
  save.json     game state (items, unlocks, docked files) — written by the game, do not hand-edit
  __builtins__.py  authoritative API reference (see below)
  sim.toml      benchmark ledger: best time + every approach tried, per resource
docs/           copy of the in-game documentation (mechanics, scripting, unlocks)
flake.nix       Linux automation devShell — see below
automation/     scripts for driving the game headlessly on this NixOS/Hyprland machine
```

There is no build, test, or lint tooling. The game is the runtime.

**Note:** the copy of `Save0/` the game actually reads at runtime is NOT this checkout — it's a
separate git clone of this same repo inside the Steam Proton compat prefix:
`~/.local/share/Steam/steamapps/compatdata/2060160/pfx/drive_c/users/steamuser/AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced/Saves`.
Edits made here don't reach the game until committed/pulled (or copied) there; the farmer-mcp server
(below) edits that live copy directly.

## Linux Automation (headless play via MCP)

`flake.nix` + `automation/*.sh` run the game inside a **private, headless Sway compositor** the real
desktop never sees — no window, no stolen focus/input, fully isolated from the actual Hyprland
session. This is what the [farmer-mcp](https://github.com/BridgerB/the-farmer-was-replaced-mcp)
server drives to give Claude Code full read/write/run control of the game.

```bash
nix develop --command automation/start-env.sh    # bring up the private compositor (idempotent)
nix develop --command automation/launch-game.sh  # launch the game into it (blocks until it exits;
                                                  # refuses if the game's already running anywhere)
nix develop --command automation/game-control.sh start|stop|status  # F5 / Shift+F5 / window check
nix develop --command automation/stop-env.sh     # tear the compositor down
```

Input is injected via `xdotool`/XTEST against the compositor's private XWayland `DISPLAY`, not
Wayland-protocol injection (`wtype`/`wlrctl`) or `ydotool`/uinput — see comments in `flake.nix` and
`automation/start-env.sh` for why (motion-only delivery, and physical-device-grab risk, respectively).
`launch-game.sh` replicates Steam's own launch command (captured via `/proc/<pid>/cmdline` from a real
launch) rather than touching Steam's binary `localconfig.vdf`; re-capture it if Steam changes the
Proton version or library layout (comment at the top of the script has the exact commands).

### `__builtins__.py` is the source of truth for the API

Shipped by the game, it contains typed stubs and full docstrings for every builtin (tick cost,
return value, example usage), plus the complete `Items`, `Entities`, `Grounds`, `Unlocks`, `Hats`,
`Leaderboards`, and direction constants. **Read it instead of guessing an API name or tick cost.**
It also gives IntelliSense in external editors; the game auto-regenerates it.

## Running Code

1. Edit `.py` files in `Save0/` — the game's **File Watcher** option picks up saves live.
   Creating or deleting a file still requires reloading the save in-game.
2. Execute a file from the in-game editor. `main.py` is the gameplay entry point.
3. `quick_print()` output lands in the game's output page / `output.txt`.

Claude cannot run this code. Verification means reading carefully and asking the user to run it.

## The Simulation Benchmark Workflow (primary activity in this repo)

`simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)` runs a file in a throwaway
world and returns the elapsed in-game seconds. The real farm is untouched. Nothing can be returned
from a simulation except that time — pass data in via `sim_globals`, get results out via
`quick_print()`.

The loop this repo follows, one resource at a time:

1. Write `Save0/sim_<resource>.py` — a **self-contained** script that farms to a target amount and
   `quick_print()`s the elapsed time. It may `import` gameplay modules (`sim_power.py` drives
   `sunflower.py`) but usually inlines its own tuned strategy.
2. Write a tiny launcher (`mcp.py`, `run_sim.py`) that calls `simulate()` with generous starting
   items, `Unlocks` (everything maxed), a fixed seed, and a high speedup, then execute the launcher
   in-game.
3. Record the result in `sim.toml` under `[<resource>]`.
4. Iterate on the strategy; commit as `feat: sim <x> baseline` then `feat: improved <x> sim`.

### `sim.toml` — read this before optimizing anything

Per-resource sections holding `seconds_to_10m` (time to farm 10,000,000 of the item; gold uses
`seconds_to_1m`) plus commented notes on the winning approach, the mechanics discovered, and — most
valuably — **every approach already tested and rejected, with its time**. Check it before proposing
an optimization; most obvious ideas have already been measured. Update it whenever a benchmark moves.

Current bests: wood 7.94s · hay 41.48s · gold 84s (to 1M) · carrot/pumpkin/cactus (see file) ·
weird_substance 249s · bone 723s · power ~65000s (estimated, the outlier worth attacking).

## Language Constraints (CRITICAL)

The in-game language resembles Python but is not Python:

- **No ternary expressions** — `x if c else y` is a syntax error; use if/else blocks
- **No f-strings** — concatenate: `"n: " + str(n)`
- **No import aliasing** (`import x as y`, `from x import y as z`) and no subdirectory imports —
  every file sits flat in `Save0/`, imported as `import nav` then `nav.go_to(...)`
- **Spawned drones cannot return data** — `spawn_drone()` workers communicate only by mutating the
  world; the spawner must re-scan afterwards
- Tuples work, including as dict keys: `{(x, y): value}`
- Files are indented with **tabs**

## Architecture

### Shared utilities

- **`nav.py`** — `go_to(x, y)`; `s_shape_range(x_start, x_end, y_start, y_end)` returns positions in
  a serpentine order (alternating columns reversed) so consecutive cells are adjacent;
  `traverse_zone(x_start, x_end, y_start, y_end, cell_fn)` walks that order calling `cell_fn(x, y)`.
- **`drone.py`** — splits the field into vertical zones, one per available drone.
  `get_zone_bounds()` returns `[x_start, x_end, y_start, y_end]` per zone (remainder columns go to
  the *first* zones). `run_parallel(worker_factory, main_fn)` is the standard entry: wait for idle,
  spawn workers for zones 1..n, run `main_fn` on zone 0, wait for all to finish.
- **`resources.py`** — `get_next_crop()` drives auto mode: bootstrap hay → wood → carrot, then keep
  power above `POWER_THRESHOLD`, carrots above `CARROT_MIN`, enough Weird_Substance for one maze
  (`size * 2**(num_unlocked(Unlocks.Mazes)-1)`), else farm whatever is lowest.
- **`logs.py`** — thin `quick_print()` wrapper (0 ticks, unlike `print()` which costs 1 real second).
- **`poly.py`** — polyculture companion bookkeeping via `get_companion()`; not yet wired into a cycle.

### Crop modules — each exports `cycle()`

`hay.py` `wood.py` `carrot.py` `pumpkin.py` `sunflower.py` `substance.py` `maze.py` (gold)
`cactus.py` `dinosaur.py` (bones). `main.py` sets a module-level `MODE` string and dispatches to
them in an infinite loop; `hamiltonian.py` and `dinosaur_tiny.py` are one-shot bone runs.

**Zone-parallel pattern** (hay, wood, carrot, substance, cactus): a `cell_fn(x, y)` doing
till/harvest/plant, a `*_zone(x_start, x_end, y_start, y_end)` wrapper, a `make_worker(...)` closure
factory taking the same four bounds, and `cycle()` calling `drone.run_parallel(make_worker, farm_zone)`.
Worker factories exist because the four bounds must be captured in a closure — spawned functions take
no arguments.

Crops with global ordering constraints break the pattern:

- **`pumpkin.py`** — every pumpkin must be fully grown before *any* is harvested; one `harvest()`
  then collects the whole merged mega-pumpkin (yield = connected count³). Water while planting.
- **`sunflower.py`** — plant in parallel recording `measure()` petal counts, then run one
  synchronized pass per petal value 15→7, so the highest-petal flowers always go first (8x power
  bonus, lost and penalized if the order breaks).
- **`cactus.py`** — plant all, wait for all, then bubble-sort the grid by `measure()` size using
  `swap(East)` / `swap(North)` (rows in parallel, then columns), and harvest (0,0) once to chain the
  whole sorted field (yield = chain length²).
- **`maze.py`** — position many drones across the field *before* the maze exists, plant a bush and
  `use_item(Items.Weird_Substance)` to spawn it, then each drone polls `measure()` (returns the
  treasure position from anywhere inside) and runs DFS-with-backtracking toward it; first to arrive
  harvests.
- **`dinosaur.py`** — snake mini-game under `Hats.Dinosaur_Hat`. BFS toward the apple with a
  reachability/tail-safety check; `hamiltonian.py` instead follows a fixed Hamiltonian cycle over a
  22–24 grid, which never self-traps and is what produced the recorded bone benchmark.

## Code Style

- Gameplay modules: no comments, small pure functions, early returns, tabs.
- `sim_*.py`: heavily commented banner-style headers documenting strategy, args, and measured
  performance — these are lab notes and are meant to be verbose.
- Guard before acting: `if get_entity_type() == None` before `plant()`, check item counts before
  planting anything that costs carrots, `drone.wait_for_workers()` before spawning a new batch.

## Performance Notes

- Actions (`move`, `plant`, `harvest`, `till`, `swap`, `use_item`, `change_hat`) cost 200 ticks;
  sensing (`get_pos_*`, `get_entity_type`, `measure`, `can_harvest`) costs 1. `quick_print()` is free.
- Holding `Items.Power` halves movement cost to 100 ticks — it is consumed automatically.
- 32 drones is the cap at full unlocks; one drone per column is the workhorse layout, and the
  benchmarks show drone throughput — not plant growth — is usually the bottleneck.
- Wrap-around movement matters: moving off an edge reappears on the opposite side, so the shortest
  path to a far column is often backwards. `sim_gold.py` depends on this.
- Skipping a `can_harvest()` check and just harvesting can be faster than checking.

## Gotchas

1. `Entities.Hay` does not exist — plant `Entities.Grass`, which yields `Items.Hay`.
2. `till()` toggles; calling it twice returns the tile to grassland.
3. Fertilized grass yields Weird_Substance, but only if fertilized *while still growing* — grass
   that is already ripe yields plain hay.
4. Dead pumpkins (~20% of plantings) can never be harvested; planting over them clears them.
5. `set_world_size()` (min 3) and `clear()` are destructive to the live farm — fine inside a
   simulation, deliberate everywhere else.
6. `Save0/CLAUDE.md` is a copy of this file kept in the save folder; update both together.
