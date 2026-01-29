def solve(tx, ty):
	visited = {}
	path = []
	while True:
		ent = get_entity_type()
		if ent == Entities.Treasure:
			harvest()
			return True
		if ent != Entities.Hedge:
			return False
		pos = (get_pos_x(), get_pos_y())
		visited[pos] = True
		moved = False
		dx = tx - get_pos_x()
		dy = ty - get_pos_y()
		dirs = []
		if abs(dx) >= abs(dy):
			if dx > 0:
				dirs.append(East)
			elif dx < 0:
				dirs.append(West)
			if dy > 0:
				dirs.append(North)
			elif dy < 0:
				dirs.append(South)
		else:
			if dy > 0:
				dirs.append(North)
			elif dy < 0:
				dirs.append(South)
			if dx > 0:
				dirs.append(East)
			elif dx < 0:
				dirs.append(West)
		for d in [North, East, South, West]:
			if d not in dirs:
				dirs.append(d)
		for d in dirs:
			if can_move(d):
				x = get_pos_x()
				y = get_pos_y()
				if d == North:
					np = (x, y + 1)
				elif d == South:
					np = (x, y - 1)
				elif d == East:
					np = (x + 1, y)
				else:
					np = (x - 1, y)
				if np not in visited:
					move(d)
					path.append(d)
					moved = True
					break
		if not moved and len(path) > 0:
			last = path.pop()
			if last == North:
				move(South)
			elif last == South:
				move(North)
			elif last == East:
				move(West)
			else:
				move(East)
		elif not moved:
			return False

def make_worker(target_x, target_y, size):
	def worker():
		dx = target_x
		dy = target_y
		if dx > size // 2:
			x_dir = West
			x_moves = size - dx
		else:
			x_dir = East
			x_moves = dx
		if dy > size // 2:
			y_dir = South
			y_moves = size - dy
		else:
			y_dir = North
			y_moves = dy
		x_moved = 0
		y_moved = 0
		while x_moved < x_moves or y_moved < y_moves:
			pos = measure()
			if pos != None:
				if get_entity_type() == Entities.Hedge:
					solve(pos[0], pos[1])
				return
			if x_moved < x_moves:
				move(x_dir)
				x_moved = x_moved + 1
			elif y_moved < y_moves:
				move(y_dir)
				y_moved = y_moved + 1
		pos = measure()
		while pos == None:
			pos = measure()
		if get_entity_type() == Entities.Hedge:
			solve(pos[0], pos[1])
	return worker

def get_distributed_positions(num_positions, size):
	if num_positions <= 0:
		return []
	cols = 1
	rows = 1
	while cols * rows < num_positions:
		if cols <= rows:
			cols = cols + 1
		else:
			rows = rows + 1
	positions = []
	for row in range(rows):
		cols_in_row = num_positions // rows
		if row < (num_positions % rows):
			cols_in_row = cols_in_row + 1
		for col in range(cols_in_row):
			px = (size * (col * 2 + 1)) // (cols_in_row * 2)
			py = (size * (row * 2 + 1)) // (rows * 2)
			positions.append((px, py))
	return positions

def run_maze():
	size = 32
	num_workers = max_drones() - 1
	positions = get_distributed_positions(num_workers, size)
	
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)
	
	for p in positions:
		spawn_drone(make_worker(p[0], p[1], size))
	
	for i in range(5):
		move(East)
	for i in range(5):
		move(West)
	
	substance_cost = size * (2 ** max(0, num_unlocked(Unlocks.Mazes) - 1))
	if get_ground_type() == Grounds.Soil:
		till()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance_cost)
	
	pos = measure()
	while pos == None:
		pos = measure()
	
	solve(pos[0], pos[1])
	
	while num_drones() > 1:
		pass

quick_print("=== FAST + HEDGE CHECK ===")

clear()
set_world_size(32)

target = 10000000
start = get_time()
maze_count = 0

while num_items(Items.Gold) < target:
	run_maze()
	maze_count = maze_count + 1
	if maze_count % 20 == 0:
		quick_print("Maze " + str(maze_count) + " at " + str(get_time() - start) + "s, gold=" + str(num_items(Items.Gold)))

total = get_time() - start
quick_print("---")
quick_print("DONE: " + str(num_items(Items.Gold)) + " gold")
quick_print("Mazes: " + str(maze_count))
quick_print("Total time: " + str(total) + "s")
quick_print("Per maze: " + str(total / maze_count) + "s")
