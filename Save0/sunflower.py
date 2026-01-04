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

	# Phase 1: Plant all sunflowers AND measure petals - ONE scan
	movement.go_to_start()
	sunflowers = []
	for i in range(total):
		if get_ground_type() != Grounds.Soil:
			till()

		if can_harvest() and get_entity_type() != Entities.Sunflower:
			harvest()

		if get_entity_type() == None:
			if num_items(Items.Carrot) > 0:
				plant(Entities.Sunflower)

		if get_entity_type() == Entities.Sunflower:
			sunflowers.append([get_pos_x(), get_pos_y(), measure()])

		movement.move_next()

	if len(sunflowers) < 10:
		return

	# Phase 2: Sort by petals descending
	for i in range(len(sunflowers)):
		for j in range(len(sunflowers) - 1):
			if sunflowers[j][2] < sunflowers[j + 1][2]:
				temp = sunflowers[j]
				sunflowers[j] = sunflowers[j + 1]
				sunflowers[j + 1] = temp

	# Phase 3: Harvest in order - wait at each until ready
	for sf in sunflowers:
		go_to(sf[0], sf[1])
		while not can_harvest():
			pass
		harvest()

def farm_sunflower():
	while True:
		farm_cycle()

if __name__ == "__main__":
	farm_sunflower()
