# -----------------------------------------------------------------------------
# Kicks off a Leaderboards.Maze competitive run.
#
# leaderboard_run() launches leaderboard_maze.py in an isolated simulation
# with fixed starting conditions (everything unlocked, 1e9 Weird_Substance,
# 1e9 Power) - it does NOT touch the live farm, same isolation as simulate().
# Runs are padded/repeated to a minimum 2 hours of in-game time; a high
# speedup collapses that to a short real-time wait.
#
# Execute this file directly from the in-game editor.
# -----------------------------------------------------------------------------
leaderboard_run(Leaderboards.Maze, "leaderboard_maze", 1000)
