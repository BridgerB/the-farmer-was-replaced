# -----------------------------------------------------------------------------
# Leaderboards.Carrots entry point.
#
# Started via leaderboard_run(Leaderboards.Carrots, "leaderboard_carrots", speedup).
# Fixed starting conditions: everything unlocked, plenty of carrot seed
# and wood/hay. Goal: farm 2,000,000,000 carrot as fast as possible, then
# TERMINATE.
#
# Does NOT loop carrot.py's cycle() - same reasoning as leaderboard_wood.py:
# repeatedly respawning worker drones (drone.run_parallel() every cycle)
# leaks memory in the engine at scale, and 2B carrot needs thousands of
# cycles regardless of world size. Uses carrot.py's run_until(goal) instead,
# which spawns each zone worker exactly ONCE and loops internally.
# -----------------------------------------------------------------------------
import carrot
import logs

GOAL = 2000000000
carrot.run_until(GOAL)

logs.log("leaderboard carrots run complete: " + str(num_items(Items.Carrot)))
