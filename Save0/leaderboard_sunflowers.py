# -----------------------------------------------------------------------------
# Leaderboards.Sunflowers entry point.
#
# Started via leaderboard_run(Leaderboards.Sunflowers, "leaderboard_sunflowers", speedup).
# Fixed starting conditions: everything unlocked, plenty of sunflower seed
# and carrots. Goal: farm 100,000 power as fast as possible, then TERMINATE.
# Reuses sunflower.py's cycle() unchanged.
#
# world_size(32) is the tuned sweet spot, confirmed by bracketing it in both
# directions:
#   - native/88 (attempt 2): memory hit 13GB in under 3 min, same OOM
#     trajectory as the original crash, for 11:42.778 - no better and much
#     riskier.
#   - 16 (attempt 3): safe, but slower - 22:37.709, since a smaller field
#     needs more compounding cycles to reach 100k power, a net loss.
#   - 32: 11:42.614, our confirmed best, safely reproducible.
# Getting meaningfully closer to the 2:21.942 world record from here would
# need a different algorithm (e.g. avoiding the 9x full-zone re-traversal
# per petal value that sunflower.py's cycle() does for the ordering
# guarantee), not further world-size tuning - that lever is exhausted.
# -----------------------------------------------------------------------------
import sunflower
import logs

set_world_size(32)
GOAL = 100000
while num_items(Items.Power) < GOAL:
	sunflower.cycle()

logs.log("leaderboard sunflowers run complete: " + str(num_items(Items.Power)))
