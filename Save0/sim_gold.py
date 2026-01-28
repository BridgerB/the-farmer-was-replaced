def get_dirs_towards(tx, ty):
	x = get_pos_x()
	y = get_pos_y()
	dirs = []
	dx = tx - x
	dy = ty - y
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
	return dirs

def opposite(d):
	if d == North:
		return South
	if d == South:
		return North
	if d == East:
		return West
	return East

def get_next_pos(d):
	x = get_pos_x()
	y = get_pos_y()
	if d == North:
		return (x, y + 1)
	if d == South:
		return (x, y - 1)
	if d == East:
		return (x + 1, y)
	return (x - 1, y)

def solve_maze(tx, ty):
	visited = {}
	path = []
	while get_entity_type() == Entities.Hedge or get_entity_type() == Entities.Treasure:
		if get_entity_type() == Entities.Treasure:
			harvest()
			return True
		pos = (get_pos_x(), get_pos_y())
		visited[pos] = True
		moved = False
		for d in get_dirs_towards(tx, ty):
			if can_move(d):
				next_pos = get_next_pos(d)
				if next_pos not in visited:
					move(d)
					path.append(d)
					moved = True
					break
		if not moved and len(path) > 0:
			last = path.pop()
			move(opposite(last))
		elif not moved:
			return False
	return False

def waiting_solver():
	while get_entity_type() != Entities.Hedge and get_entity_type() != Entities.Treasure:
		pass
	pos = measure()
	if pos != None:
		solve_maze(pos[0], pos[1])

def run_maze_multi():
	size = get_world_size()
	substance_cost = size * (2 ** max(0, num_unlocked(Unlocks.Mazes) - 1))
	
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)
	
	corners = [(size-1, 0), (0, size-1), (size-1, size-1)]
	for cx, cy in corners:
		while get_pos_x() < cx:
			move(East)
		while get_pos_x() > cx:
			move(West)
		while get_pos_y() < cy:
			move(North)
		while get_pos_y() > cy:
			move(South)
		spawn_drone(waiting_solver)
	
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)
	
	if get_ground_type() == Grounds.Soil:
		till()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance_cost)
	
	pos = measure()
	if pos != None:
		solve_maze(pos[0], pos[1])
	
	while num_drones() > 1:
		pass

quick_print("=== FULL 10M TEST (32x32 multi-drone) ===")
clear()
set_world_size(32)

start = get_time()
mazes = 0
while num_items(Items.Gold) < 10000000:
	run_maze_multi()
	mazes = mazes + 1
	if mazes % 20 == 0:
		quick_print("Progress: " + str(num_items(Items.Gold)) + " gold, " + str(mazes) + " mazes")

total = get_time() - start
quick_print("DONE: " + str(total) + "s for " + str(num_items(Items.Gold)) + " gold (" + str(mazes) + " mazes)")
