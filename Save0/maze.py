def go_to_origin():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

def opposite(direction):
	if direction == North:
		return South
	elif direction == South:
		return North
	elif direction == East:
		return West
	else:
		return East

def get_next_pos(direction):
	x = get_pos_x()
	y = get_pos_y()
	if direction == North:
		return (x, y + 1)
	elif direction == South:
		return (x, y - 1)
	elif direction == East:
		return (x + 1, y)
	else:
		return (x - 1, y)

def get_directions_towards(tx, ty):
	# Return directions sorted by which gets us closer to target
	x = get_pos_x()
	y = get_pos_y()
	dirs = []

	# Prioritize directions that move towards treasure
	if tx > x:
		dirs.append(East)
	if tx < x:
		dirs.append(West)
	if ty > y:
		dirs.append(North)
	if ty < y:
		dirs.append(South)

	# Add remaining directions
	for d in [North, East, South, West]:
		if d not in dirs:
			dirs.append(d)

	return dirs

def solve_maze():
	# Smart pathfinding using measure() to know treasure location
	visited = []
	path = []
	max_steps = 10000

	# Get treasure position
	tx, ty = measure()

	steps = 0
	while get_entity_type() != Entities.Treasure and steps < max_steps:
		steps = steps + 1
		pos = (get_pos_x(), get_pos_y())
		if pos not in visited:
			visited.append(pos)

		# Get directions prioritized towards treasure
		directions = get_directions_towards(tx, ty)

		# Try each direction, preferring ones towards treasure
		moved = False
		for direction in directions:
			if can_move(direction):
				next_pos = get_next_pos(direction)
				if next_pos not in visited:
					move(direction)
					path.append(direction)
					moved = True
					break

		# Dead end - backtrack
		if not moved and len(path) > 0:
			last = path.pop()
			move(opposite(last))
		elif not moved and len(path) == 0:
			break

	harvest()

def farm_cycle():
	# If already in a maze, just solve it
	if get_entity_type() == Entities.Hedge or get_entity_type() == Entities.Treasure:
		solve_maze()
		return

	size = get_world_size()
	substance_needed = size * (2 ** max(0, num_unlocked(Unlocks.Mazes) - 1))

	# Check if we have enough weird substance
	if num_items(Items.Weird_Substance) < substance_needed:
		return

	go_to_origin()

	# Prepare ground
	if get_ground_type() == Grounds.Soil:
		till()

	# Plant bush
	plant(Entities.Bush)

	# Create maze
	use_item(Items.Weird_Substance, substance_needed)

	# Solve it
	solve_maze()

def farm_maze():
	while True:
		farm_cycle()

if __name__ == "__main__":
	farm_maze()
