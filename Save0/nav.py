def go_to(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

def s_shape_range(start_col, end_col, size):
	positions = []
	for col in range(start_col, end_col):
		if (col - start_col) % 2 == 0:
			for y in range(size):
				positions.append([col, y])
		else:
			for y in range(size - 1, -1, -1):
				positions.append([col, y])
	return positions

def traverse_zone(start_col, end_col, cell_fn):
	size = get_world_size()
	for pos in s_shape_range(start_col, end_col, size):
		go_to(pos[0], pos[1])
		cell_fn(pos[0], pos[1])
