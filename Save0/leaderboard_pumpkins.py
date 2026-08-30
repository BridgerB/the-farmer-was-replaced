# -----------------------------------------------------------------------------
# Leaderboards.Pumpkins entry point.
#
# Started via leaderboard_run(Leaderboards.Pumpkins, "leaderboard_pumpkins", speedup).
# Fixed starting conditions: everything unlocked, plenty of pumpkin seed
# and carrots/power. Goal: farm 200,000,000 pumpkin as fast as possible,
# then TERMINATE. Reuses pumpkin.py's cycle() unchanged.
# -----------------------------------------------------------------------------
import pumpkin
import logs

GOAL = 200000000
while num_items(Items.Pumpkin) < GOAL:
	pumpkin.cycle()

logs.log("leaderboard pumpkins run complete: " + str(num_items(Items.Pumpkin)))
