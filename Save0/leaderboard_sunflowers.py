# -----------------------------------------------------------------------------
# Leaderboards.Sunflowers entry point.
#
# Started via leaderboard_run(Leaderboards.Sunflowers, "leaderboard_sunflowers", speedup).
# Fixed starting conditions: everything unlocked, plenty of sunflower seed
# and carrots. Goal: farm 100,000 power as fast as possible, then TERMINATE.
# Reuses sunflower.py's cycle() unchanged.
# -----------------------------------------------------------------------------
import sunflower
import logs

GOAL = 100000
while num_items(Items.Power) < GOAL:
	sunflower.cycle()

logs.log("leaderboard sunflowers run complete: " + str(num_items(Items.Power)))
