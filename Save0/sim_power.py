# =============================================================================
# POWER FARMING BASELINE
# =============================================================================
# Uses existing sunflower.py module which has optimized parallel harvesting
# =============================================================================

import sunflower

clear()
start_power = num_items(Items.Power)
start_time = get_time()
target = 10000000
cycles = 0

quick_print("=== POWER FARMING (using sunflower.py) ===")
quick_print("Grid: " + str(get_world_size()) + "x" + str(get_world_size()))
quick_print("Target: " + str(target) + " power")

while num_items(Items.Power) < target:
	sunflower.cycle()
	cycles = cycles + 1
	
	if cycles % 5 == 0:
		elapsed = get_time() - start_time
		gained = num_items(Items.Power) - start_power
		rate = gained / elapsed
		quick_print(str(cycles) + " cycles: " + str(gained) + " power (" + str(rate) + "/s)")

total_time = get_time() - start_time
total_gained = num_items(Items.Power) - start_power

quick_print("---")
quick_print("DONE: " + str(num_items(Items.Power)) + " power")
quick_print("Cycles: " + str(cycles))
quick_print("Total time: " + str(total_time) + "s")
quick_print("Rate: " + str(total_gained / total_time) + " power/sec")
