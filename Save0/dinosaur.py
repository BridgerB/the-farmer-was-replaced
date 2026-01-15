import logs
import nav

def get_next_position(x, y, direction):
	if direction == North:
		return (x, y + 1)
	if direction == South:
		return (x, y - 1)
	if direction == East:
		return (x + 1, y)
	return (x - 1, y)

def is_in_bounds(x, y, grid_size):
	return x >= 0 and x < grid_size and y >= 0 and y < grid_size

def is_tail_blocking_full(x, y, tail):
	for i in range(len(tail)):
		if tail[i][0] == x and tail[i][1] == y:
			return True
	return False

def is_tail_blocking(x, y, tail):
	if len(tail) == 0:
		return False
	for i in range(len(tail) - 1):
		if tail[i][0] == x and tail[i][1] == y:
			return True
	return False

def find_path_bfs(start_x, start_y, target_x, target_y, tail, grid_size):
	if start_x == target_x and start_y == target_y:
		return []
	visited = {}
	visited[(start_x, start_y)] = True
	parent = {}
	parent[(start_x, start_y)] = None
	queue = [(start_x, start_y)]
	qi = 0
	found = False
	while qi < len(queue):
		cx, cy = queue[qi]
		qi = qi + 1
		for d in [North, East, South, West]:
			nx, ny = get_next_position(cx, cy, d)
			if not is_in_bounds(nx, ny, grid_size):
				continue
			if is_tail_blocking(nx, ny, tail):
				continue
			if (nx, ny) in visited:
				continue
			visited[(nx, ny)] = True
			parent[(nx, ny)] = (cx, cy, d)
			if nx == target_x and ny == target_y:
				found = True
				break
			queue.append((nx, ny))
		if found:
			break
	if not found:
		return None
	path = []
	cur = (target_x, target_y)
	while parent[cur] != None:
		px, py, d = parent[cur]
		path.append(d)
		cur = (px, py)
	rev = []
	for i in range(len(path) - 1, -1, -1):
		rev.append(path[i])
	return rev

def simulate_moves(start_x, start_y, moves, tail, new_tail_len):
	sx, sy = start_x, start_y
	sim_tail = []
	for seg in tail:
		sim_tail.append(seg)
	for d in moves:
		sim_tail.insert(0, (sx, sy))
		while len(sim_tail) > new_tail_len:
			sim_tail.pop()
		sx, sy = get_next_position(sx, sy, d)
	return (sx, sy, sim_tail)

def can_reach_tail(x, y, tail, grid_size):
	if len(tail) == 0:
		return True
	tail_end_x = tail[len(tail) - 1][0]
	tail_end_y = tail[len(tail) - 1][1]
	path = find_path_bfs(x, y, tail_end_x, tail_end_y, tail, grid_size)
	return path != None

def count_reachable(x, y, tail, grid_size):
	visited = {}
	visited[(x, y)] = True
	queue = [(x, y)]
	qi = 0
	count = 1
	while qi < len(queue):
		cx, cy = queue[qi]
		qi = qi + 1
		for d in [North, East, South, West]:
			nx, ny = get_next_position(cx, cy, d)
			if not is_in_bounds(nx, ny, grid_size):
				continue
			if is_tail_blocking(nx, ny, tail):
				continue
			if (nx, ny) in visited:
				continue
			visited[(nx, ny)] = True
			queue.append((nx, ny))
			count = count + 1
	return count

def chase_apples():
	grid_size = get_world_size()
	total_cells = grid_size * grid_size

	num_apples = 0
	tail = []
	cached_path = []
	apple_x = -1
	apple_y = -1
	moves_since_apple = 0

	while True:
		my_x = get_pos_x()
		my_y = get_pos_y()

		if get_entity_type() == Entities.Apple:
			num_apples = num_apples + 1
			cached_path = []
			moves_since_apple = 0

			info = measure()
			if info != None:
				apple_x = info[0]
				apple_y = info[1]

				bfs_path = find_path_bfs(my_x, my_y, apple_x, apple_y, tail, grid_size)
				if bfs_path != None and len(bfs_path) > 0:
					fx, fy, ft = simulate_moves(my_x, my_y, bfs_path, tail, num_apples + 1)
					if can_reach_tail(fx, fy, ft, grid_size):
						cached_path = bfs_path

				logs.log("APPLE " + str(num_apples) + " path=" + str(len(cached_path)))
			else:
				apple_x = -1
				apple_y = -1

		if len(cached_path) > 0:
			next_dir = cached_path[0]
			cached_path = cached_path[1:]
		else:
			found_path = False
			if apple_x >= 0 and apple_y >= 0:
				bfs_path = find_path_bfs(my_x, my_y, apple_x, apple_y, tail, grid_size)
				if bfs_path != None and len(bfs_path) > 0:
					fx, fy, ft = simulate_moves(my_x, my_y, bfs_path, tail, num_apples + 1)
					if can_reach_tail(fx, fy, ft, grid_size):
						cached_path = bfs_path
						next_dir = cached_path[0]
						cached_path = cached_path[1:]
						found_path = True
					elif moves_since_apple > total_cells * 2:
						cached_path = [bfs_path[0]]
						next_dir = cached_path[0]
						cached_path = cached_path[1:]
						found_path = True

			if not found_path:
				found_move = False
				if len(tail) > 0:
					tail_end_x = tail[len(tail) - 1][0]
					tail_end_y = tail[len(tail) - 1][1]
					for d in [North, East, South, West]:
						ax, ay = get_next_position(my_x, my_y, d)
						if ax == tail_end_x and ay == tail_end_y:
							next_dir = d
							found_move = True
							break
					if not found_move:
						chase_path = find_path_bfs(my_x, my_y, tail_end_x, tail_end_y, tail, grid_size)
						if chase_path != None and len(chase_path) > 0:
							next_dir = chase_path[0]
							found_move = True

				if not found_move:
					best_dir = None
					best_reach = -1
					for d in [North, East, South, West]:
						ax, ay = get_next_position(my_x, my_y, d)
						if not is_in_bounds(ax, ay, grid_size):
							continue
						if is_tail_blocking(ax, ay, tail):
							continue
						sim_tail = [(my_x, my_y)]
						for seg in tail:
							sim_tail.append(seg)
						while len(sim_tail) > num_apples:
							sim_tail.pop()
						reachable = count_reachable(ax, ay, sim_tail, grid_size)
						if reachable > best_reach:
							best_reach = reachable
							best_dir = d
					if best_dir != None:
						next_dir = best_dir
					else:
						logs.log("TRAPPED at " + str(my_x) + "," + str(my_y) + " apples=" + str(num_apples))
						return False

		nx, ny = get_next_position(my_x, my_y, next_dir)
		tail_growing = len(tail) < num_apples
		if tail_growing:
			is_blocked = is_tail_blocking_full(nx, ny, tail)
		else:
			is_blocked = is_tail_blocking(nx, ny, tail)
		if is_blocked:
			best_safe_dir = None
			best_safe_reach = -1
			for d in [North, East, South, West]:
				tx, ty = get_next_position(my_x, my_y, d)
				if not is_in_bounds(tx, ty, grid_size):
					continue
				if tail_growing:
					cell_blocked = is_tail_blocking_full(tx, ty, tail)
				else:
					cell_blocked = is_tail_blocking(tx, ty, tail)
				if not cell_blocked:
					sim_tail = [(my_x, my_y)]
					for seg in tail:
						sim_tail.append(seg)
					while len(sim_tail) > num_apples:
						sim_tail.pop()
					reach = count_reachable(tx, ty, sim_tail, grid_size)
					if reach > best_safe_reach:
						best_safe_reach = reach
						best_safe_dir = d
			if best_safe_dir != None:
				next_dir = best_safe_dir
			else:
				logs.log("TRAPPED at " + str(my_x) + "," + str(my_y) + " apples=" + str(num_apples))
				return False

		if not move(next_dir):
			logs.log("MOVE FAILED at " + str(my_x) + "," + str(my_y) + " dir=" + str(next_dir) + " apples=" + str(num_apples))
			logs.log("tail len=" + str(len(tail)) + " tail_growing=" + str(tail_growing))
			for d in [North, East, South, West]:
				tx, ty = get_next_position(my_x, my_y, d)
				inb = is_in_bounds(tx, ty, grid_size)
				blk = False
				blkf = False
				if inb:
					blk = is_tail_blocking(tx, ty, tail)
					blkf = is_tail_blocking_full(tx, ty, tail)
				logs.log("  " + str(d) + " -> " + str(tx) + "," + str(ty) + " inb=" + str(inb) + " blk=" + str(blk) + " blkf=" + str(blkf))
			return False

		tail.insert(0, (my_x, my_y))
		while len(tail) > num_apples:
			tail.pop()
		moves_since_apple = moves_since_apple + 1

	return True

def cycle():
	logs.log("Starting dinosaur")
	if num_items(Items.Cactus) < 100:
		return True
	nav.go_to(0, 0)
	if get_entity_type() != None:
		harvest()
	change_hat(Hats.Dinosaur_Hat)
	success = chase_apples()
	change_hat(Hats.Straw_Hat)
	if not success:
		logs.log("FAILED")
	return success
