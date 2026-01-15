import logs
import nav

def cycle():
	set_world_size(22)
	grid = get_world_size()
	total = grid * grid

	nav.go_to(0, 0)
	if get_entity_type() != None:
		harvest()

	change_hat(Hats.Dinosaur_Hat)

	logs.log("Starting Hamiltonian on " + str(grid) + "x" + str(grid) + " = " + str(total) + " cells")

	stuck = False
	cycles = 0

	while not stuck:
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

		if not move(West):
			stuck = True
			break

		for i in range(grid - 1):
			if not move(South):
				stuck = True
				break

	change_hat(Hats.Straw_Hat)

	bones = num_items(Items.Bone)
	logs.log("Hamiltonian done: " + str(cycles) + " cycles")
	logs.log("Total bones: " + str(bones))
