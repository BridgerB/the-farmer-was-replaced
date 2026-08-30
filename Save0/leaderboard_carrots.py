# -----------------------------------------------------------------------------
# Leaderboards.Carrots entry point.
#
# Started via leaderboard_run(Leaderboards.Carrots, "leaderboard_carrots", speedup).
# Fixed starting conditions: everything unlocked, plenty of carrot seed
# and wood/hay. Goal: farm 2,000,000,000 carrot as fast as possible, then
# TERMINATE. Reuses carrot.py's cycle() unchanged.
#
# Defensive: force size 32 like the other categories (see leaderboard_wood.py
# for why - Cactus and Sunflowers both OOM-crashed the game via
# leaderboard_run()'s auto-retry-leaks-memory failure mode despite looking
# safe beforehand).
# -----------------------------------------------------------------------------
import carrot
import logs

set_world_size(32)
GOAL = 2000000000
while num_items(Items.Carrot) < GOAL:
	carrot.cycle()

logs.log("leaderboard carrots run complete: " + str(num_items(Items.Carrot)))
