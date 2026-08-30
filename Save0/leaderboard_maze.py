# -----------------------------------------------------------------------------
# Leaderboards.Maze entry point.
#
# Started via leaderboard_run(Leaderboards.Maze, "leaderboard_maze", speedup)
# (see run_leaderboard_maze.py). Fixed starting conditions per
# docs/unlocks/leaderboard.md: everything unlocked, 1e9 Weird_Substance and
# 1e9 Power. Goal: farm 9,863,168 gold (= one 32x32 maze reused 300 times)
# as fast as possible, then TERMINATE - the run is only scored once the
# program actually ends.
#
# Reuses maze.py's cycle() unchanged - it already handles substance
# top-ups via substance.cycle() as a fallback, though with 1e9 starting
# Weird_Substance that fallback should never trigger here.
#
# IMPORTANT: the leaderboard's fixed starting conditions unlock everything,
# which means get_world_size() defaults to the MAX (88) rather than the 32
# the target amount is calibrated for ("one 32x32 maze reused 300 times").
# An 88x88 maze is dramatically more expensive to solve and needs far more
# substance per cycle - confirmed this stalled a real run for 4+ hours of
# CPU time with zero result. Force size 32 to match the intended benchmark.
# -----------------------------------------------------------------------------
import maze
import logs

GOAL = 9863168

set_world_size(32)
while num_items(Items.Gold) < GOAL:
	maze.cycle()

logs.log("leaderboard maze run complete: " + str(num_items(Items.Gold)))
