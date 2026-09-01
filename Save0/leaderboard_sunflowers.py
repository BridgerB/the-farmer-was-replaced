# -----------------------------------------------------------------------------
# Leaderboards.Sunflowers entry point.
#
# Started via leaderboard_run(Leaderboards.Sunflowers, "leaderboard_sunflowers", speedup).
# Fixed starting conditions: everything unlocked, plenty of sunflower seed
# and carrots. Goal: farm 100,000 power as fast as possible, then TERMINATE.
# Reuses sunflower.py's cycle() unchanged.
#
# ATTEMPT 2 (racing for a faster time, not just a safe completion): reverting
# the world_size(32) force from attempt 1. Re-examined output.txt from that
# original world-88 crash - it showed a continuous single run (no repeated
# "run complete" line), the same signature as Wood/Carrot/Hay's leak, NOT
# the auto-retry-on-instant-completion pattern confirmed for Cactus. So the
# real fix is the same one that worked for Wood: fewer, bigger cycles (native
# world size) means FEWER total drone spawns overall, not more - each
# sunflower.cycle() call still needs 9 synchronized respawn passes (one per
# petal value, required for the highest-petal-first bonus order), but at
# world 88 only ~3-4 cycles are needed to reach 100k power vs ~7-10 at
# world 32, so total spawns are lower despite each cycle spawning more.
# World record is 2:21.942; our world_size(32) run got 11:42.614 - trying
# for something much closer.
# -----------------------------------------------------------------------------
import sunflower
import logs

GOAL = 100000
while num_items(Items.Power) < GOAL:
	sunflower.cycle()

logs.log("leaderboard sunflowers run complete: " + str(num_items(Items.Power)))
