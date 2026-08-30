# -----------------------------------------------------------------------------
# Leaderboards.Carrots entry point.
#
# Started via leaderboard_run(Leaderboards.Carrots, "leaderboard_carrots", speedup).
# Fixed starting conditions: everything unlocked, plenty of carrot seed
# and wood/hay. Goal: farm 2,000,000,000 carrot as fast as possible, then
# TERMINATE. Reuses carrot.py's cycle() unchanged.
# -----------------------------------------------------------------------------
import carrot
import logs

GOAL = 2000000000
while num_items(Items.Carrot) < GOAL:
	carrot.cycle()

logs.log("leaderboard carrots run complete: " + str(num_items(Items.Carrot)))
