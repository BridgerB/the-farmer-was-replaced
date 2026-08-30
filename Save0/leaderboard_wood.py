# -----------------------------------------------------------------------------
# Leaderboards.Wood entry point.
#
# Started via leaderboard_run(Leaderboards.Wood, "leaderboard_wood", speedup).
# Fixed starting conditions: everything unlocked, plenty of wood/power.
# Goal: farm 10,000,000,000 wood as fast as possible, then TERMINATE.
# Reuses wood.py's cycle() unchanged.
#
# REVERTED the set_world_size(32) forcing added after the Cactus/Sunflowers
# crashes - that diagnosis doesn't apply here. Confirmed via output.txt: the
# Wood run OOM-crashed the game (journalctl: RSS ~24GB) after ~6 minutes
# with ONLY "wood cycle" log lines - never a single "run complete", so this
# isn't leaderboard_run()'s auto-retry-on-fast-completion leak at all. It
# looks like spawning/despawning worker drones at high frequency leaks
# memory in the engine regardless of category, and forcing size 32 made it
# WORSE here: each cycle's yield is ~(32/88)^2 smaller, so reaching the 10B
# goal needs far MORE cycles (more total drone spawns) than at native size.
# sim.toml records single-tree harvests yielding ~409,600 wood at native
# size - leave world size at its full-unlock default to keep total cycles
# (and drone spawns) as low as possible.
# -----------------------------------------------------------------------------
import wood
import logs

GOAL = 10000000000
while num_items(Items.Wood) < GOAL:
	wood.cycle()

logs.log("leaderboard wood run complete: " + str(num_items(Items.Wood)))
