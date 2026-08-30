# -----------------------------------------------------------------------------
# Leaderboards.Cactus entry point.
#
# Started via leaderboard_run(Leaderboards.Cactus, "leaderboard_cactus", speedup).
# Fixed starting conditions: everything unlocked, plenty of cactus seed and
# power. Goal: farm 33,554,432 cactus as fast as possible, then TERMINATE.
# Reuses cactus.py's cycle() unchanged.
# -----------------------------------------------------------------------------
import cactus
import logs

GOAL = 33554432
while num_items(Items.Cactus) < GOAL:
	cactus.cycle()

logs.log("leaderboard cactus run complete: " + str(num_items(Items.Cactus)))
