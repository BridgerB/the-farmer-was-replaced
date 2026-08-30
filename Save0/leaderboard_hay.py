# -----------------------------------------------------------------------------
# Leaderboards.Hay entry point.
#
# Started via leaderboard_run(Leaderboards.Hay, "leaderboard_hay", speedup).
# Fixed starting conditions: everything unlocked, plenty of hay/power.
# Goal: farm 2,000,000,000 hay as fast as possible, then TERMINATE.
# Reuses hay.py's cycle() unchanged.
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
import hay
import logs

GOAL = 2000000000
while num_items(Items.Hay) < GOAL:
	hay.cycle()

logs.log("leaderboard hay run complete: " + str(num_items(Items.Hay)))
