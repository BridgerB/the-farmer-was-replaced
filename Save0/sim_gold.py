TARGET = 10000000

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

def solve_maze(tx, ty):
	visited = {}
	path = []
	while True:
		entity = get_entity_type()
		if entity == Entities.Treasure:
			harvest()
			return True
		if entity != Entities.Hedge:
			return False
		
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

def run_maze():
	size = get_world_size()
	substance_cost = size * (2 ** max(0, num_unlocked(Unlocks.Mazes) - 1))
	
	if num_items(Items.Weird_Substance) < substance_cost:
		return False
	
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)
	
	if get_ground_type() == Grounds.Soil:
		till()
	
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance_cost)
	tx, ty = measure()
	solve_maze(tx, ty)
	return True

clear()
set_world_size(10)
start = get_time()
size = get_world_size()

quick_print("=== GOLD SIM (10x10 baseline) ===")

mazes = 0
while num_items(Items.Gold) < TARGET:
	if not run_maze():
		quick_print("OUT OF SUBSTANCE at " + str(mazes) + " mazes")
		break
	mazes = mazes + 1
	
	if mazes <= 10 or mazes % 500 == 0:
		elapsed = get_time() - start
		quick_print("M" + str(mazes) + ": " + str(num_items(Items.Gold)) + " gold @" + str(elapsed) + "s")

elapsed = get_time() - start
quick_print("")
quick_print("=== RESULTS ===")
quick_print("Gold: " + str(num_items(Items.Gold)))
quick_print("Mazes: " + str(mazes))
quick_print("Time: " + str(elapsed) + "s")
