# -----------------------------------------------------------------------------
# Leaderboards.Sunflowers entry point.
#
# Started via leaderboard_run(Leaderboards.Sunflowers, "leaderboard_sunflowers", speedup).
# Fixed starting conditions: everything unlocked, plenty of sunflower seed
# and carrots. Goal: farm 100,000 power as fast as possible, then TERMINATE.
# Reuses sunflower.py's cycle() unchanged.
#
# IMPORTANT: the 8x highest-petal-first bonus makes power compound fast per
# cycle (observed 0->1033->8191 in consecutive cycles on the full-unlock
# default world size 88). That reaches the 100k goal in only ~4 cycles,
# fast enough that leaderboard_run()'s auto-retry-for-a-longer-benchmark
# mechanic fires repeatedly and leaks memory each pass, same failure mode
# as Cactus (see leaderboard_cactus.py) - confirmed via journalctl OOM-
# killing the game (RSS ~24GB) about 3-4 minutes after this run started.
# Force size 32 so a full-field cycle yields less, spacing out completions.
# -----------------------------------------------------------------------------
import sunflower
import logs

set_world_size(32)
GOAL = 100000
while num_items(Items.Power) < GOAL:
	sunflower.cycle()

logs.log("leaderboard sunflowers run complete: " + str(num_items(Items.Power)))
