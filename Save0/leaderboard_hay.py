# -----------------------------------------------------------------------------
# Leaderboards.Hay entry point.
#
# Started via leaderboard_run(Leaderboards.Hay, "leaderboard_hay", speedup).
# Fixed starting conditions: everything unlocked, plenty of hay/power.
# Goal: farm 2,000,000,000 hay as fast as possible, then TERMINATE.
# Reuses hay.py's cycle() unchanged.
#
# Defensive: force size 32 like the other categories (see leaderboard_wood.py
# for why - Cactus and Sunflowers both OOM-crashed the game via
# leaderboard_run()'s auto-retry-leaks-memory failure mode despite looking
# safe beforehand).
# -----------------------------------------------------------------------------
import hay
import logs

set_world_size(32)
GOAL = 2000000000
while num_items(Items.Hay) < GOAL:
	hay.cycle()

logs.log("leaderboard hay run complete: " + str(num_items(Items.Hay)))
