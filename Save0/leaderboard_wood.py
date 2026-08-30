# -----------------------------------------------------------------------------
# Leaderboards.Wood entry point.
#
# Started via leaderboard_run(Leaderboards.Wood, "leaderboard_wood", speedup).
# Fixed starting conditions: everything unlocked, plenty of wood/power.
# Goal: farm 10,000,000,000 wood as fast as possible, then TERMINATE.
#
# Does NOT use wood.py's cycle() in a loop - that respawns a fresh batch of
# worker drones every single call via drone.run_parallel(), and each
# spawn_drone() call appears to leak memory in the engine (confirmed via
# journalctl: two separate OOM kills, RSS ~24GB each time, one at world
# size 32 and one at native/88 - same ceiling either way, just reached at
# different progress/time). Reaching 10B wood needs thousands of cycles
# regardless of per-cycle yield, so thousands of respawns was always going
# to hit that ceiling.
#
# Uses wood.py's run_until(goal) instead: spawns each zone worker exactly
# ONCE, and each worker loops internally (checking the shared goal itself)
# rather than being respawned every pass. Total drone spawns drops from
# thousands to ~31 (one per zone), which should stay well under the leak
# threshold no matter how long the run takes.
# -----------------------------------------------------------------------------
import wood
import logs

GOAL = 10000000000
wood.run_until(GOAL)

logs.log("leaderboard wood run complete: " + str(num_items(Items.Wood)))
