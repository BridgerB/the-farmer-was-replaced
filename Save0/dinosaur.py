import logs
import nav
import drone

def clear_cell(x, y):
	if get_entity_type() != None:
		harvest()

def clear_zone(x_start, x_end, y_start, y_end):
	nav.traverse_zone(x_start, x_end, y_start, y_end, clear_cell)

def make_clear_worker(x_start, x_end, y_start, y_end):
	def worker():
		clear_zone(x_start, x_end, y_start, y_end)
	return worker

def dir_name(d):
	if d == North:
		return "N"
	if d == South:
		return "S"
	if d == East:
		return "E"
	if d == West:
		return "W"
	return "?"

def find_path(start_x, start_y, target_x, target_y, tail, size):
	if start_x == target_x and start_y == target_y:
		return []
	blocked = {}
	for i in range(1, len(tail)):
		blocked[tail[i]] = True
	parent = {}
	parent[(start_x, start_y)] = None
	queue = [(start_x, start_y)]
	found = False
	visited_count = 0
	while len(queue) > 0:
		x, y = queue[0]
		queue = queue[1:]
		visited_count = visited_count + 1
		if visited_count % 100 == 0:
			quick_print("BFS visited " + str(visited_count) + " at (" + str(x) + "," + str(y) + ")")
		for d in [North, East, South, West]:
			nx, ny = x, y
			if d == North:
				ny = y + 1
			elif d == South:
				ny = y - 1
			elif d == East:
				nx = x + 1
			else:
				nx = x - 1
			if nx < 0 or nx >= size or ny < 0 or ny >= size:
				continue
			if (nx, ny) in blocked:
				continue
			if (nx, ny) in parent:
				continue
			parent[(nx, ny)] = (x, y, d)
			if nx == target_x and ny == target_y:
				found = True
				break
			queue.append((nx, ny))
		if found:
			break
	quick_print("BFS done: visited=" + str(visited_count) + " found=" + str(found))
	if not found:
		return None
	path = []
	cx, cy = target_x, target_y
	while parent[(cx, cy)] != None:
		px, py, d = parent[(cx, cy)]
		path.append(d)
		cx, cy = px, py
	reversed_path = []
	for i in range(len(path) - 1, -1, -1):
		reversed_path.append(path[i])
	return reversed_path

def chase_apples():
	size = get_world_size()
	tail = []
	apples = 0
	target_x = -1
	target_y = -1
	planned_path = []
	move_count = 0
	while True:
		x = get_pos_x()
		y = get_pos_y()
		quick_print("move " + str(move_count) + " pos=(" + str(x) + "," + str(y) + ") apples=" + str(apples))
		if get_entity_type() == Entities.Apple:
			apples = apples + 1
			target_x, target_y = measure()
			quick_print("ATE! next=(" + str(target_x) + "," + str(target_y) + ")")
			planned_path = find_path(x, y, target_x, target_y, tail, size)
			if planned_path == None:
				quick_print("NO PATH!")
				break
			path_str = ""
			for d in planned_path:
				path_str = path_str + dir_name(d)
			quick_print("PATH=" + path_str)
		if len(planned_path) == 0:
			quick_print("STUCK")
			break
		d = planned_path[0]
		planned_path = planned_path[1:]
		if move(d):
			tail.append((x, y))
			while len(tail) > apples:
				tail.pop(0)
			move_count = move_count + 1
		else:
			quick_print("MOVE FAILED! tail=" + str(tail))
			break
	logs.log("done: " + str(apples) + " apples")

def cycle():
	logs.log("dinosaur cycle")
	if num_items(Items.Cactus) < 100:
		logs.log("need cactus")
		return
	if get_entity_type() == Entities.Hedge or get_entity_type() == Entities.Treasure:
		harvest()
		return
	drone.run_parallel(make_clear_worker, clear_zone)
	nav.go_to(0, 0)
	if get_entity_type() != None:
		harvest()
	change_hat(Hats.Dinosaur_Hat)
	chase_apples()
	change_hat(Hats.Straw_Hat)
