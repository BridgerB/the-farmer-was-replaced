import logs
import dinosaur

def nav_go_to_0_0():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

def test_hamiltonian(size):
	set_world_size(size)
	grid = get_world_size()

	nav_go_to_0_0()
	if get_entity_type() != None:
		harvest()

	change_hat(Hats.Dinosaur_Hat)
	start_ticks = get_tick_count()

	total_cells = grid * grid
	cycles = 0
	max_cycles = total_cells + 10
	stuck = False

	while not stuck and cycles < max_cycles:
		cycles = cycles + 1

		for i in range(grid - 1):
			if not move(East):
				stuck = True
				break

		if stuck:
			break

		for row in range(1, grid):
			if not move(North):
				stuck = True
				break

			if row % 2 == 1:
				for i in range(grid - 2):
					if not move(West):
						stuck = True
						break
			else:
				for i in range(grid - 2):
					if not move(East):
						stuck = True
						break

			if stuck:
				break

		if stuck:
			break

		if not move(East):
			stuck = True
			break

		for i in range(grid - 1):
			if not move(South):
				stuck = True
				break

	logs.log("Ham size " + str(size) + ": " + str(cycles) + " cycles completed")

	change_hat(Hats.Straw_Hat)
	end_ticks = get_tick_count()
	return end_ticks - start_ticks

def test_bfs_chase(size):
	set_world_size(size)

	nav_go_to_0_0()
	if get_entity_type() != None:
		harvest()

	change_hat(Hats.Dinosaur_Hat)
	start_ticks = get_tick_count()

	dinosaur.chase_apples()

	change_hat(Hats.Straw_Hat)
	end_ticks = get_tick_count()
	return end_ticks - start_ticks

def cycle():
	logs.log("=== DINO STRATEGY COMPARISON ===")
	logs.log("")

	for size in [3, 5]:
		if num_items(Items.Cactus) < 200:
			logs.log("Not enough cactus for tests")
			return

		bones_before = num_items(Items.Bone)

		logs.log("--- Size " + str(size) + " ---")

		ticks1 = test_hamiltonian(size)
		bones1 = num_items(Items.Bone) - bones_before
		bones_before = num_items(Items.Bone)

		ticks2 = test_bfs_chase(size)
		bones2 = num_items(Items.Bone) - bones_before
		bones_before = num_items(Items.Bone)

		logs.log("Hamiltonian: " + str(bones1) + " bones, " + str(ticks1) + " ticks")
		logs.log("BFS Chase:   " + str(bones2) + " bones, " + str(ticks2) + " ticks")

		if ticks1 > 0:
			r1 = (bones1 * 1000) // ticks1
		else:
			r1 = 0
		if ticks2 > 0:
			r2 = (bones2 * 1000) // ticks2
		else:
			r2 = 0
		logs.log("Ratios: Ham=" + str(r1) + " BFS=" + str(r2))
		logs.log("")

	logs.log("=== DONE ===")
