import movement

def go_to(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

def plant_and_measure_zone(start_col, end_col):
	size = get_world_size()
	sunflowers = []

	for col in range(start_col, end_col):
		if (col - start_col) % 2 == 0:
			y_range = range(size)
		else:
			y_range = range(size - 1, -1, -1)

		for y in y_range:
			go_to(col, y)

			if get_ground_type() != Grounds.Soil:
				till()

			entity = get_entity_type()
			if entity != None and entity != Entities.Sunflower:
				harvest()

			if get_entity_type() == None:
				if num_items(Items.Carrot) > 0:
					plant(Entities.Sunflower)

			if get_entity_type() == Entities.Sunflower:
				petals = measure()
				sunflowers.append([col, y, petals])

	return sunflowers

def wait_for_sunflowers(sunflowers):
	not_ready = []
	for sf in sunflowers:
		not_ready.append(sf)

	while len(not_ready) > 0:
		still_waiting = []
		for sf in not_ready:
			go_to(sf[0], sf[1])
			if get_entity_type() == Entities.Sunflower and not can_harvest():
				still_waiting.append(sf)
		not_ready = still_waiting

def harvest_all_for_petals(start_x, start_y, target_petals):
	# Scan entire field from starting position, harvest matching petals
	# Loop until a full pass finds nothing
	size = get_world_size()

	found_any = True
	while found_any:
		found_any = False
		for offset in range(size * size):
			x = (start_x + offset // size) % size
			y = (start_y + offset % size) % size
			go_to(x, y)
			if get_entity_type() == Entities.Sunflower:
				if measure() == target_petals and can_harvest():
					harvest()
					found_any = True

# Plant phase worker
def plant_worker_drone(start_col, end_col):
	sunflowers = plant_and_measure_zone(start_col, end_col)
	wait_for_sunflowers(sunflowers)

def make_plant_worker(start_col, end_col):
	def worker():
		plant_worker_drone(start_col, end_col)
	return worker

# Harvest phase worker - scans entire field from a starting position
def make_harvest_worker(start_x, start_y, target_petals):
	def worker():
		harvest_all_for_petals(start_x, start_y, target_petals)
	return worker

def spawn_plant_workers():
	size = get_world_size()
	total_drones = max_drones()
	cols_per_drone = size // total_drones
	if cols_per_drone < 1:
		cols_per_drone = 1

	for i in range(1, total_drones):
		start = i * cols_per_drone
		if i == total_drones - 1:
			end = size
		else:
			end = start + cols_per_drone
		spawn_drone(make_plant_worker(start, end))

def spawn_harvest_workers(target_petals):
	# Spawn workers with staggered starting positions
	size = get_world_size()
	total_drones = max_drones()

	# Worker starting positions: spread across field
	# Worker 1: top-right corner
	# Worker 2: bottom-left corner
	# Worker 3: bottom-right corner
	starts = [
		[size - 1, 0],
		[0, size - 1],
		[size - 1, size - 1]
	]

	for i in range(1, total_drones):
		if i - 1 < len(starts):
			start_x = starts[i - 1][0]
			start_y = starts[i - 1][1]
		else:
			start_x = (i * size // total_drones) % size
			start_y = (i * size // total_drones) % size
		spawn_drone(make_harvest_worker(start_x, start_y, target_petals))

def farm_cycle():
	size = get_world_size()
	total_drones = max_drones()
	cols_per_drone = size // total_drones
	if cols_per_drone < 1:
		cols_per_drone = 1

	# Wait for any existing drones
	while num_drones() > 1:
		pass

	# PLANT PHASE - all drones plant and measure, wait for growth
	spawn_plant_workers()
	my_sunflowers = plant_and_measure_zone(0, cols_per_drone)
	wait_for_sunflowers(my_sunflowers)

	# Wait for workers to finish planting/waiting
	while num_drones() > 1:
		pass

	# HARVEST PHASE - all drones hunt entire field for each petal count
	for target_petals in range(15, 6, -1):
		spawn_harvest_workers(target_petals)
		# Main starts from (0, 0)
		harvest_all_for_petals(0, 0, target_petals)

		# Wait for workers to finish this petal round
		while num_drones() > 1:
			pass

def farm_sunflower():
	while True:
		farm_cycle()

if __name__ == "__main__":
	farm_sunflower()
