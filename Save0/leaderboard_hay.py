# -----------------------------------------------------------------------------
# Leaderboards.Hay entry point.
#
# Started via leaderboard_run(Leaderboards.Hay, "leaderboard_hay", speedup).
# Fixed starting conditions: everything unlocked, plenty of hay/power.
# Goal: farm 2,000,000,000 hay as fast as possible, then TERMINATE.
# Reuses hay.py's cycle() unchanged.
# -----------------------------------------------------------------------------
import hay
import logs

GOAL = 2000000000
while num_items(Items.Hay) < GOAL:
	hay.cycle()

logs.log("leaderboard hay run complete: " + str(num_items(Items.Hay)))
