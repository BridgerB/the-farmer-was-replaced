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

def farm_cycle():
	size = get_world_size()
	total = size * size

	# Early exit if no carrots - let main.py switch to carrot farming
	if num_items(Items.Carrot) == 0:
		return

	# Phase 1: Plant pumpkins everywhere
	movement.go_to_start()
	not_ready = []

	for i in range(total):
		# If out of carrots mid-grid, exit early and let main.py get more
		if num_items(Items.Carrot) == 0:
			return

		# Till
		if get_ground_type() != Grounds.Soil:
			till()

		# Water
		if get_water() < 0.8 and num_items(Items.Water) > 0:
			use_item(Items.Water)

		# Harvest non-pumpkins
		if can_harvest() and get_entity_type() != Entities.Pumpkin:
			harvest()

		# Plant pumpkin
		plant(Entities.Pumpkin)

		not_ready.append([get_pos_x(), get_pos_y()])
		movement.move_next()

	# Phase 2: Wait for all to be ready
	while len(not_ready) > 0:
		still_not_ready = []

		for pos in not_ready:
			go_to(pos[0], pos[1])

			if get_water() < 0.8 and num_items(Items.Water) > 0:
				use_item(Items.Water)

			if can_harvest():
				pass  # Ready
			else:
				# Not ready - try to plant (handles dead pumpkins)
				if num_items(Items.Carrot) > 0:
					plant(Entities.Pumpkin)
				still_not_ready.append(pos)

		# Abort if out of carrots and have dead pumpkins
		if len(still_not_ready) > 0 and num_items(Items.Carrot) == 0:
			return

		not_ready = still_not_ready

	# Phase 3: Harvest
	movement.go_to_start()
	harvest()

def farm_pumpkin():
	while True:
		farm_cycle()

if __name__ == "__main__":
	farm_pumpkin()
