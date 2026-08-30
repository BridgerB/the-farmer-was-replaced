# -----------------------------------------------------------------------------
# Leaderboards.Cactus entry point.
#
# Started via leaderboard_run(Leaderboards.Cactus, "leaderboard_cactus", speedup).
# Fixed starting conditions: everything unlocked, plenty of cactus seed and
# power. Goal: farm 33,554,432 cactus as fast as possible, then TERMINATE.
# Reuses cactus.py's cycle() unchanged.
#
# IMPORTANT: cactus yield is (chain length)^2. Full-unlock starting
# conditions default get_world_size() to 88, so one fully-chained cycle()
# call can yield up to 88*88=7744 -> 7744^2 ~= 60M, blowing straight past
# the goal in a single call. leaderboard_run() then auto-retries for a
# longer benchmark, but items aren't reset to 0 fast enough to notice - each
# retry re-instant-completes, and the retries leak memory until the OS OOM-
# kills the game (confirmed via journalctl: RSS hit ~24GB). Force size 32
# (max single-cycle yield 1024^2 ~= 1.05M, well under the goal) so the run
# actually takes multiple cycles like it's supposed to.
# -----------------------------------------------------------------------------
import cactus
import logs

set_world_size(32)
GOAL = 33554432
while num_items(Items.Cactus) < GOAL:
	cactus.cycle()

logs.log("leaderboard cactus run complete: " + str(num_items(Items.Cactus)))
