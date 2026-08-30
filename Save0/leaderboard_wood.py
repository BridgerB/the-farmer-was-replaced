# -----------------------------------------------------------------------------
# Leaderboards.Wood entry point.
#
# Started via leaderboard_run(Leaderboards.Wood, "leaderboard_wood", speedup).
# Fixed starting conditions: everything unlocked, plenty of wood/power.
# Goal: farm 10,000,000,000 wood as fast as possible, then TERMINATE.
# Reuses wood.py's cycle() unchanged.
#
# Defensive: force size 32 like the other categories. Wood's per-cycle
# yield is roughly linear in cell count (not squared/cubed/multiplier-
# compounding like Cactus/Pumpkin/Sunflowers), so it's unlikely to complete
# in a handful of cycles regardless of world size given the 10B goal - but
# after getting burned twice by "should be safe" assumptions (Cactus,
# Sunflowers both OOM-crashed the game via leaderboard_run()'s auto-retry
# leak), force it anyway rather than risk a third crash.
# -----------------------------------------------------------------------------
import wood
import logs

set_world_size(32)
GOAL = 10000000000
while num_items(Items.Wood) < GOAL:
	wood.cycle()

logs.log("leaderboard wood run complete: " + str(num_items(Items.Wood)))
