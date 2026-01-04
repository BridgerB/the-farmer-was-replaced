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

def plant_zone(start_col, end_col):
	size = get_world_size()

	for col in range(start_col, end_col):
		if (col - start_col) % 2 == 0:
			y_range = range(size)
		else:
			y_range = range(size - 1, -1, -1)

		for y in y_range:
			go_to(col, y)

			if get_ground_type() != Grounds.Soil:
				till()

			if get_water() < 0.8 and num_items(Items.Water) > 0:
				use_item(Items.Water)

			if get_entity_type() != Entities.Pumpkin:
				if can_harvest():
					harvest()
				if num_items(Items.Carrot) > 0:
					plant(Entities.Pumpkin)

def verify_zone(start_col, end_col):
	size = get_world_size()

	plant_zone(start_col, end_col)

	not_ready = []
	for col in range(start_col, end_col):
		if (col - start_col) % 2 == 0:
			y_range = range(size)
		else:
			y_range = range(size - 1, -1, -1)

		for y in y_range:
			go_to(col, y)

			if get_water() < 0.8 and num_items(Items.Water) > 0:
				use_item(Items.Water)

			if get_entity_type() == Entities.Pumpkin and can_harvest():
				# Ready!
				pass
			elif get_entity_type() == Entities.Pumpkin:
				# Growing
				not_ready.append([col, y])
			else:
				# No pumpkin
				if can_harvest():
					harvest()
				if num_items(Items.Carrot) > 0:
					plant(Entities.Pumpkin)
					not_ready.append([col, y])

	while len(not_ready) > 0:
		still_not_ready = []

		for pos in not_ready:
			go_to(pos[0], pos[1])

			if get_water() < 0.8 and num_items(Items.Water) > 0:
				use_item(Items.Water)

			if get_entity_type() == Entities.Pumpkin and can_harvest():
				# Ready! Don't add to still_not_ready
				pass
			elif get_entity_type() == Entities.Pumpkin:
				# Growing, keep waiting
				still_not_ready.append(pos)
			else:
				# No pumpkin - try to plant
				if can_harvest():
					harvest()
				if num_items(Items.Carrot) > 0:
					plant(Entities.Pumpkin)
					still_not_ready.append(pos)
				# If no carrots and no pumpkin, skip this spot

		not_ready = still_not_ready

	return True

def worker_drone(start_col, end_col):
	verify_zone(start_col, end_col)

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

def harvester_drone(start_col, end_col):
	while True:
		# Exit if out of carrots to let main.py farm more
		if num_items(Items.Carrot) == 0:
			return

		verify_zone(start_col, end_col)

		while num_drones() > 1:
			pass

		harvest()
		go_to(0, 0)

		spawn_workers()

def farm_cycle():
	size = get_world_size()

	if num_items(Items.Carrot) == 0:
		return

	total_drones = max_drones()
	cols_per_drone = size // total_drones
	if cols_per_drone < 1:
		cols_per_drone = 1

	spawn_workers()
	# Main does first zone (columns 0 to cols_per_drone)
	harvester_drone(0, cols_per_drone)

def farm_pumpkin():
	while True:
		farm_cycle()

if __name__ == "__main__":
	farm_pumpkin()
