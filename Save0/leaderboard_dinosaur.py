# -----------------------------------------------------------------------------
# Leaderboards.Dinosaur entry point.
#
# Started via leaderboard_run(Leaderboards.Dinosaur, "leaderboard_dinosaur", speedup).
# Fixed starting conditions per docs/unlocks/leaderboard.md: everything
# unlocked, 1e9 Cactus and 1e9 Power. Goal: farm 33,488,928 bone (= filling
# a 32x32 area with the dinosaur tail) as fast as possible, then TERMINATE.
#
# REWRITE: the first version of this file used a hand-rolled greedy heuristic
# (chase apple, then own tail, then any free direction) with NO stall/self-trap
# bound. It ran for 7.5+ real hours with zero completed lives and had to be
# killed - unlike dinosaur.py's chase_apples_hamiltonian, a plain greedy chase
# has no guarantee it ever gets stuck OR ever finishes cleanly, so there was no
# way to tell "still working" from "will never terminate".
#
# Reuses dinosaur.py's cycle() unchanged instead - it's the proven, *bounded*
# algorithm (real Hamiltonian cycle walk with tail-safe shortcuts, max_moves
# and stall_limit caps) that produced the recorded bone benchmark in sim.toml.
#
# IMPORTANT: same world_size issue as leaderboard_maze.py - full-unlock
# starting conditions default get_world_size() to the MAX (88), not the 32
# the target amount is calibrated for. Force size 32.
# -----------------------------------------------------------------------------
import dinosaur
import logs

set_world_size(32)
GOAL = 33488928
while num_items(Items.Bone) < GOAL:
	dinosaur.cycle()
	logs.log("leaderboard dinosaur: bone=" + str(num_items(Items.Bone)))

logs.log("leaderboard dinosaur run complete: " + str(num_items(Items.Bone)))
