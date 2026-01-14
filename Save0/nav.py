def go_to(x, y):
	while get_pos_x() < x:
		if not move(East):
			break
	while get_pos_x() > x:
		if not move(West):
			break
	while get_pos_y() < y:
		if not move(North):
			break
	while get_pos_y() > y:
		if not move(South):
			break

def s_shape_range(x_start, x_end, y_start, y_end):
	positions = []
	for col in range(x_start, x_end):
		if (col - x_start) % 2 == 0:
			for y in range(y_start, y_end):
				positions.append([col, y])
		else:
			for y in range(y_end - 1, y_start - 1, -1):
				positions.append([col, y])
	return positions

def traverse_zone(x_start, x_end, y_start, y_end, cell_fn):
	for pos in s_shape_range(x_start, x_end, y_start, y_end):
		go_to(pos[0], pos[1])
		cell_fn(pos[0], pos[1])
