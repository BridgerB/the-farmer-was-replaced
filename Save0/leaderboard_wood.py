# -----------------------------------------------------------------------------
# Leaderboards.Wood entry point.
#
# Started via leaderboard_run(Leaderboards.Wood, "leaderboard_wood", speedup).
# Fixed starting conditions: everything unlocked, plenty of wood/power.
# Goal: farm 10,000,000,000 wood as fast as possible, then TERMINATE.
# Reuses wood.py's cycle() unchanged.
# -----------------------------------------------------------------------------
import wood
import logs

GOAL = 10000000000
while num_items(Items.Wood) < GOAL:
	wood.cycle()

logs.log("leaderboard wood run complete: " + str(num_items(Items.Wood)))
