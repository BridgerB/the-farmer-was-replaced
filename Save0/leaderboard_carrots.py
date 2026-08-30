# -----------------------------------------------------------------------------
# Leaderboards.Carrots entry point.
#
# Started via leaderboard_run(Leaderboards.Carrots, "leaderboard_carrots", speedup).
# Fixed starting conditions: everything unlocked, plenty of carrot seed
# and wood/hay. Goal: farm 2,000,000,000 carrot as fast as possible, then
# TERMINATE. Reuses carrot.py's cycle() unchanged.
#
# NOT forcing set_world_size(32) here - see leaderboard_wood.py. That "fix"
# (added defensively after Cactus/Sunflowers OOM-crashed) turned out to be
# wrong for large-target categories: the Wood run crashed anyway with only
# continuous "wood cycle" logs (never a repeat/retry), pointing to a plain
# drone-spawn-frequency memory leak rather than the auto-retry pathology.
# Forcing a smaller world size only multiplies the number of cycles (and
# drone spawns) needed to reach a multi-billion goal, making it worse.
# Leave world size at its full-unlock default to minimize total cycles.
# -----------------------------------------------------------------------------
import carrot
import logs

GOAL = 2000000000
while num_items(Items.Carrot) < GOAL:
	carrot.cycle()

logs.log("leaderboard carrots run complete: " + str(num_items(Items.Carrot)))
