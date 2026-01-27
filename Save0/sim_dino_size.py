import logs

def calc_ticks_for_size(world_size):
	total_cells = world_size * world_size
	ticks = 400
	total_ticks = 0
	for i in range(total_cells):
		total_ticks = total_ticks + ticks
		ticks = ticks - (ticks * 3) // 100
	return total_ticks

def test_world_size(size):
	set_world_size(size)
	grid = get_world_size()
	total_cells = grid * grid

	nav_go_to_0_0()
	if get_entity_type() != None:
		harvest()

	change_hat(Hats.Dinosaur_Hat)

	start_ticks = get_tick_count()
	apples = 0

	for row in range(grid):
		if row % 2 == 0:
			for col in range(grid - 1):
				move(East)
				if get_entity_type() == Entities.Apple:
					apples = apples + 1
		else:
			for col in range(grid - 1):
				move(West)
				if get_entity_type() == Entities.Apple:
					apples = apples + 1
		if row < grid - 1:
			move(North)
			if get_entity_type() == Entities.Apple:
				apples = apples + 1

	change_hat(Hats.Straw_Hat)

	end_ticks = get_tick_count()
	used_ticks = end_ticks - start_ticks
	bones = apples * apples

	if used_ticks > 0:
		ratio = (bones * 1000000) // used_ticks
	else:
		ratio = 0

	logs.log("Size " + str(size) + ": apples=" + str(apples) + "/" + str(total_cells) + " bones=" + str(bones) + " ticks=" + str(used_ticks) + " ratio=" + str(ratio))
	return (bones, used_ticks, ratio)

def nav_go_to_0_0():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

def cycle():
	logs.log("=== DINO SIZE SIMULATION ===")
	logs.log("Testing different world sizes (S-pattern, no pathfinding)")
	logs.log("")

	for size in [3, 5, 7, 10]:
		if num_items(Items.Cactus) >= 100:
			test_world_size(size)

	logs.log("")
	logs.log("=== DONE ===")
	