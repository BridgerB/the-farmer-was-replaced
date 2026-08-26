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
# -----------------------------------------------------------------------------
import maze
import logs

GOAL = 9863168

while num_items(Items.Gold) < GOAL:
	maze.cycle()

logs.log("leaderboard maze run complete: " + str(num_items(Items.Gold)))
