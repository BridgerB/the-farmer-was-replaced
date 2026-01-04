# Shared movement functions

def go_to_start():
	# Go to top-left corner (0, size-1)
	size = get_world_size()
	while get_pos_x() != 0:
		move(West)
	while get_pos_y() != size - 1:
		move(North)

def move_next():
	# Snake pattern based on actual position
	size = get_world_size()
	x = get_pos_x()
	y = get_pos_y()

	# Top row goes East, next row goes West, etc.
	going_east = (size - 1 - y) % 2 == 0

	if going_east:
		if x == size - 1:
			move(South)
		else:
			move(East)
	else:
		if x == 0:
			move(South)
		else:
			move(West)

def traverse_all(tile_func):
	# Go to start, process each tile with tile_func, move in snake pattern
	size = get_world_size()
	go_to_start()
	for i in range(size * size):
		tile_func()
		move_next()
		