import nav
import logs
import substance

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

def solve_with_target(tx, ty, gold_before):
	visited = {}
	path = []
	moves = 0
	max_moves = get_world_size() * get_world_size() * 4
	while get_entity_type() == Entities.Hedge or get_entity_type() == Entities.Treasure:
		if get_entity_type() == Entities.Treasure:
			harvest()
			return True
		if num_items(Items.Gold) > gold_before:
			logs.log("maze: treasure already claimed elsewhere, giving up")
			return False
		moves = moves + 1
		if moves > max_moves:
			logs.log("maze: solver exceeded move cap, giving up")
			return False
		pos = (get_pos_x(), get_pos_y())
		if pos not in visited:
			visited[pos] = True
		priority_dirs = get_directions_towards(tx, ty)
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
	return False

def make_solver_with_target(tx, ty, gold_before):
	def solver():
		solve_with_target(tx, ty, gold_before)
	return solver

def make_waiting_solver(tx, ty, gold_before):
	def solver():
		while get_entity_type() != Entities.Hedge and get_entity_type() != Entities.Treasure:
			if num_items(Items.Gold) > gold_before:
				return
			pass
		solve_with_target(tx, ty, gold_before)
	return solver

def solve_maze_from_here():
	tx, ty = measure()
	size = get_world_size()
	gold_before = num_items(Items.Gold)
	corners = [
		(size - 1, 0),
		(0, size - 1),
		(size - 1, size - 1),
	]
	for corner in corners:
		if num_drones() < max_drones():
			spawn_drone(make_solver_with_target(tx, ty, gold_before))
	solve_with_target(tx, ty, gold_before)

def cycle():
	logs.log("maze cycle")
	if get_entity_type() == Entities.Hedge or get_entity_type() == Entities.Treasure:
		solve_maze_from_here()
		return
	size = get_world_size()
	substance_needed = size * (2 ** max(0, num_unlocked(Unlocks.Mazes) - 1))
	if num_items(Items.Weird_Substance) < substance_needed:
		logs.log("maze: substance low (have " + str(num_items(Items.Weird_Substance)) + ", need " + str(substance_needed) + "), farming substance")
		substance.cycle()
		return
	nav.go_to(0, 0)
	if get_ground_type() == Grounds.Soil:
		till()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance_needed)
	tx, ty = measure()
	gold_before = num_items(Items.Gold)
	corners = [
		(size - 1, 0),
		(0, size - 1),
		(size - 1, size - 1),
	]
	for corner in corners:
		if num_drones() < max_drones():
			nav.go_to(corner[0], corner[1])
			spawn_drone(make_waiting_solver(tx, ty, gold_before))
	nav.go_to(0, 0)
	solve_with_target(tx, ty, gold_before)
