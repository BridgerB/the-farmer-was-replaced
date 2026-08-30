# -----------------------------------------------------------------------------
# Leaderboards.Hay entry point.
#
# Started via leaderboard_run(Leaderboards.Hay, "leaderboard_hay", speedup).
# Fixed starting conditions: everything unlocked, plenty of hay/power.
# Goal: farm 2,000,000,000 hay as fast as possible, then TERMINATE.
#
# Does NOT loop hay.py's cycle() - same reasoning as leaderboard_wood.py:
# repeatedly respawning worker drones (drone.run_parallel() every cycle)
# leaks memory in the engine at scale, and 2B hay needs thousands of cycles
# regardless of world size. Uses hay.py's run_until(goal) instead, which
# spawns each zone worker exactly ONCE and loops internally.
# -----------------------------------------------------------------------------
import hay
import logs

GOAL = 2000000000
hay.run_until(GOAL)

logs.log("leaderboard hay run complete: " + str(num_items(Items.Hay)))
