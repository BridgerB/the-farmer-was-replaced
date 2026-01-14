import logs
import nav

def find_path_to_apple(sx, sy, ax, ay, tail, apples, size):
	if sx == ax and sy == ay:
		return []

	queue = []
	queue.append((sx, sy, [], []))
	visited = {}
	visited[(sx, sy)] = True

	while len(queue) > 0:
		cx, cy, dirs, positions = queue[0]
		queue = queue[1:]

		for d in [North, East, South, West]:
			nx, ny = cx, cy
			if d == North:
				ny = cy + 1
			elif d == South:
				ny = cy - 1
			elif d == East:
				nx = cx + 1
			else:
				nx = cx - 1

			if nx < 0 or nx >= size or ny < 0 or ny >= size:
				continue
			if (nx, ny) in visited:
				continue

			steps = len(dirs) + 1
			tail_len = len(tail)
			blocked = False

			remaining_tail = tail_len - steps
			if remaining_tail > 0:
				for i in range(remaining_tail):
					if tail[i] == (nx, ny):
						blocked = True
						break

			if not blocked:
				for p in positions:
					if p == (nx, ny):
						blocked = True
						break
			if not blocked:
				if (sx, sy) == (nx, ny):
					blocked = True

			if blocked:
				continue

			new_dirs = []
			for dd in dirs:
				new_dirs.append(dd)
			new_dirs.append(d)

			new_pos = []
			for p in positions:
				new_pos.append(p)
			new_pos.append((cx, cy))

			if nx == ax and ny == ay:
				return new_dirs

			visited[(nx, ny)] = True
			queue.append((nx, ny, new_dirs, new_pos))

	return None

def path_to_tail(sx, sy, tail, path_so_far, size):
	if len(tail) == 0:
		return True

	steps = len(path_so_far)
	tail_len = len(tail)

	remaining = tail_len - steps
	if remaining <= 0:
		return True

	target_x = tail[remaining - 1][0]
	target_y = tail[remaining - 1][1]

	blocked = {}
	for i in range(remaining - 1):
		blocked[tail[i]] = True
	for p in path_so_far:
		blocked[p] = True

	if sx == target_x and sy == target_y:
		return True

	visited = {}
	visited[(sx, sy)] = True
	queue = [(sx, sy)]
	head = 0

	while head < len(queue):
		cx, cy = queue[head]
		head = head + 1
		for d in [North, East, South, West]:
			nx, ny = cx, cy
			if d == North:
				ny = cy + 1
			elif d == South:
				ny = cy - 1
			elif d == East:
				nx = cx + 1
			else:
				nx = cx - 1
			if nx < 0 or nx >= size or ny < 0 or ny >= size:
				continue
			if (nx, ny) in blocked:
				continue
			if (nx, ny) in visited:
				continue
			if nx == target_x and ny == target_y:
				return True
			visited[(nx, ny)] = True
			queue.append((nx, ny))
	return False

def chase_apples():
	size = get_world_size()
	apples = 0
	apple_x = -1
	apple_y = -1
	tail = []
	planned_path = []

	while True:
		x = get_pos_x()
		y = get_pos_y()

		if get_entity_type() == Entities.Apple:
			apples = apples + 1
			apple_pos = measure()
			apple_x = apple_pos[0]
			apple_y = apple_pos[1]
			planned_path = find_path_to_apple(x, y, apple_x, apple_y, tail, apples, size)
			if planned_path == None:
				logs.log("no path to apple")
				break

		if apple_x == -1:
			break

		if len(planned_path) == 0:
			logs.log("empty path")
			break

		d = planned_path[0]
		planned_path = planned_path[1:]

		if not move(d):
			logs.log("move failed")
			break

		tail.insert(0, (x, y))
		while len(tail) > apples:
			tail.pop()

	logs.log("done: " + str(apples) + " apples")

def cycle():
	logs.log("dinosaur cycle")
	if num_items(Items.Cactus) < 100:
		logs.log("need cactus")
		return
	nav.go_to(0, 0)
	if get_entity_type() != None:
		harvest()
	change_hat(Hats.Dinosaur_Hat)
	chase_apples()
	change_hat(Hats.Straw_Hat)
