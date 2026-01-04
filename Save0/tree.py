import movement

def process_tile():
	# Harvest if ready
	if can_harvest():
		harvest()

	# Checkerboard pattern for trees (no adjacent = no slowdown)
	x = get_pos_x()
	y = get_pos_y()
	if not can_harvest():
		if (x + y) % 2 == 0:
			plant(Entities.Tree)
		else:
			plant(Entities.Bush)

def farm_cycle():
	movement.traverse_all(process_tile)

def farm_tree():
	while True:
		farm_cycle()

if __name__ == "__main__":
	farm_tree()
