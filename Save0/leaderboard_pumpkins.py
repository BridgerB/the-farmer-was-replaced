# -----------------------------------------------------------------------------
# Leaderboards.Pumpkins entry point.
#
# Started via leaderboard_run(Leaderboards.Pumpkins, "leaderboard_pumpkins", speedup).
# Fixed starting conditions: everything unlocked, plenty of pumpkin seed
# and carrots/power. Goal: farm 200,000,000 pumpkin as fast as possible,
# then TERMINATE. Reuses pumpkin.py's cycle() unchanged.
#
# IMPORTANT: pumpkin yield is (connected count)^3, same risk class as Cactus
# (see leaderboard_cactus.py) - a full-unlock world defaults to size 88, and
# one fully-merged mega-pumpkin there (~7744 cells) would yield ~4.6e11,
# instantly blowing past the goal and triggering leaderboard_run()'s auto-
# retry-until-it-leaks-memory-and-OOMs failure mode (confirmed on Cactus via
# journalctl - RSS hit ~24GB before the kernel killed the game). Force size
# 32: even a full 1024-cell merge (~1.07e9) still exceeds the 200M goal in
# one shot, so this doesn't fully eliminate the risk the way it did for
# Cactus - watch this run closely at the start for the failure signature
# (output.txt showing "run complete" repeating rapidly with no popup).
# -----------------------------------------------------------------------------
import pumpkin
import logs

set_world_size(32)
GOAL = 200000000
while num_items(Items.Pumpkin) < GOAL:
	pumpkin.cycle()

logs.log("leaderboard pumpkins run complete: " + str(num_items(Items.Pumpkin)))
