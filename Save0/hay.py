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

def farm_zone(start_col, end_col):
	# One pass through zone in S-shape
	size = get_world_size()

	for col in range(start_col, end_col):
		if (col - start_col) % 2 == 0:
			y_range = range(size)
		else:
			y_range = range(size - 1, -1, -1)

		for y in y_range:
			go_to(col, y)

			if can_harvest():
				harvest()

			if get_ground_type() == Grounds.Soil:
				till()

			if get_entity_type() == None:
				plant(Entities.Grass)

def worker_drone(start_col, end_col):
	# One pass then exit
	farm_zone(start_col, end_col)

def make_worker(start_col, end_col):
	def worker():
		worker_drone(start_col, end_col)
	return worker

def spawn_workers():
	size = get_world_size()
	total_drones = max_drones()
	cols_per_drone = size // total_drones
	if cols_per_drone < 1:
		cols_per_drone = 1

	for i in range(1, total_drones):
		start = i * cols_per_drone
		if i == total_drones - 1:
			end = size  # Last worker covers remainder
		else:
			end = start + cols_per_drone
		spawn_drone(make_worker(start, end))

def farm_cycle():
	size = get_world_size()

	total_drones = max_drones()
	cols_per_drone = size // total_drones
	if cols_per_drone < 1:
		cols_per_drone = 1

	# Wait for any existing drones to finish
	while num_drones() > 1:
		pass

	spawn_workers()

	# Main does first zone (columns 0 to cols_per_drone)
	farm_zone(0, cols_per_drone)

	# Wait for workers to finish
	while num_drones() > 1:
		pass

def farm_hay():
	while True:
		farm_cycle()

if __name__ == "__main__":
	farm_hay()
