import nav
import logs

def opposite(direction):
	if direction == North:
		return South
	if direction == South:
		return North
	if direction == East:
		return West
	return East

def get_next_pos(direction):
	x = get_pos_x()
	y = get_pos_y()
	if direction == North:
		return (x, y + 1)
	if direction == South:
		return (x, y - 1)
	if direction == East:
		return (x + 1, y)
	return (x - 1, y)

def get_directions_towards(tx, ty):
	x = get_pos_x()
	y = get_pos_y()
	dirs = []
	if tx > x:
		dirs.append(East)
	if tx < x:
		dirs.append(West)
	if ty > y:
		dirs.append(North)
	if ty < y:
		dirs.append(South)
	for d in [North, East, South, West]:
		if d not in dirs:
			dirs.append(d)
	return dirs

def solve_from_pos(priority_dirs):
	visited = {}
	path = []
	while get_entity_type() == Entities.Hedge or get_entity_type() == Entities.Treasure:
		if get_entity_type() == Entities.Treasure:
			harvest()
			return
		pos = (get_pos_x(), get_pos_y())
		if pos not in visited:
			visited[pos] = True
		moved = False
		for direction in priority_dirs:
			if can_move(direction):
				next_pos = get_next_pos(direction)
				if next_pos not in visited:
					move(direction)
					path.append(direction)
					moved = True
					break
		if not moved and len(path) > 0:
			last = path.pop()
			move(opposite(last))
		elif not moved:
			break

def make_solver(priority_dirs):
	def solver():
		solve_from_pos(priority_dirs)
	return solver

def make_waiting_solver(priority_dirs):
	def solver():
		while get_entity_type() != Entities.Hedge and get_entity_type() != Entities.Treasure:
			pass
		solve_from_pos(priority_dirs)
	return solver

def solve_maze_from_here():
	tx, ty = measure()
	strategies = [
		[North, East, South, West],
		[East, South, West, North],
		[South, West, North, East],
	]
	for strat in strategies:
		if num_drones() < max_drones():
			spawn_drone(make_solver(strat))
	dirs = get_directions_towards(tx, ty)
	solve_from_pos(dirs)

def cycle():
	logs.log("maze cycle")
	if get_entity_type() == Entities.Hedge or get_entity_type() == Entities.Treasure:
		solve_maze_from_here()
		return
	size = get_world_size()
	substance_needed = size * (2 ** max(0, num_unlocked(Unlocks.Mazes) - 1))
	if num_items(Items.Weird_Substance) < substance_needed:
		return
	corners = [
		[size - 1, 0, [North, West, South, East]],
		[0, size - 1, [South, East, North, West]],
		[size - 1, size - 1, [South, West, North, East]],
	]
	for corner in corners:
		if num_drones() < max_drones():
			nav.go_to(corner[0], corner[1])
			spawn_drone(make_waiting_solver(corner[2]))
	nav.go_to(0, 0)
	if get_ground_type() == Grounds.Soil:
		till()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance_needed)
	tx, ty = measure()
	dirs = get_directions_towards(tx, ty)
	solve_from_pos(dirs)
