# -----------------------------------------------------------------------------
# Leaderboards.Sunflowers entry point.
#
# Started via leaderboard_run(Leaderboards.Sunflowers, "leaderboard_sunflowers", speedup).
# Fixed starting conditions: everything unlocked, plenty of sunflower seed
# and carrots. Goal: farm 100,000 power as fast as possible, then TERMINATE.
# Reuses sunflower.py's cycle() unchanged.
#
# world_size(32) is REQUIRED, not just defensive - tried reverting to native
# size once (attempt 2, see git history): memory hit 13GB in under 3 minutes
# (same OOM trajectory as the original crash) for a best time of 11:42.778,
# statistically the same as 32's 11:42.614. Bigger world doesn't buy a
# faster time here, only more crash risk.
#
# ATTEMPT 3: trying SMALLER (16) instead of bigger. Strictly less total work
# per cycle (fewer cells to till/plant/traverse/harvest across all 9 petal
# passes) than 32, so this should be lower risk than attempt 2's revert, not
# higher - the open question is whether a smaller field still compounds
# power fast enough per cycle to reach 100k without needing so many more
# cycles that it's a net loss. Best so far: 11:42.614. World record: 2:21.942.
# -----------------------------------------------------------------------------
import sunflower
import logs

set_world_size(16)
GOAL = 100000
while num_items(Items.Power) < GOAL:
	sunflower.cycle()

logs.log("leaderboard sunflowers run complete: " + str(num_items(Items.Power)))
