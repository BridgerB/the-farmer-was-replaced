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

def get_dir_to(x, y, tx, ty):
	if tx > x:
		return East
	if tx < x:
		return West
	if ty > y:
		return North
	if ty < y:
		return South
	return None

def is_safe_shortcut(curr_idx, target_idx, tail_indices, total):
	if target_idx == (curr_idx + 1) % total:
		return True
	if target_idx <= curr_idx:
		return False
	if len(tail_indices) == 0:
		return True
	for t_idx in tail_indices:
		if curr_idx < t_idx < target_idx:
			return False
	return True

def chase_apples():
	size = get_world_size()
	total = size * size
	path = []
	for col in range(size):
		if col % 2 == 0:
			for row in range(size):
				path.append((col, row))
		else:
			for row in range(size - 1, -1, -1):
				path.append((col, row))
	path_idx = {}
	for i in range(total):
		path_idx[path[i]] = i
	tail = []
	apples = 0
	target_x = -1
	target_y = -1
	move_count = 0
	while True:
		x = get_pos_x()
		y = get_pos_y()
		curr_idx = path_idx[(x, y)]
		quick_print("pos=(" + str(x) + "," + str(y) + ") idx=" + str(curr_idx) + " apples=" + str(apples))
		if get_entity_type() == Entities.Apple:
			apples = apples + 1
			target_x, target_y = measure()
			quick_print("ATE! next=(" + str(target_x) + "," + str(target_y) + ")")
		tail_indices = []
		for pos in tail:
			tail_indices.append(path_idx[pos])
		quick_print("tail_idx=" + str(tail_indices))
		moved = False
		if target_x >= 0 and target_x < size and target_y >= 0 and target_y < size:
			target_idx = path_idx[(target_x, target_y)]
			best_dir = None
			best_idx = -1
			for try_d in [North, East, South, West]:
				if try_d == North:
					nx, ny = x, y + 1
				elif try_d == South:
					nx, ny = x, y - 1
				elif try_d == East:
					nx, ny = x + 1, y
				else:
					nx, ny = x - 1, y
				if nx < 0 or nx >= size or ny < 0 or ny >= size:
					continue
				next_idx = path_idx[(nx, ny)]
				if not is_safe_shortcut(curr_idx, next_idx, tail_indices, total):
					continue
				if next_idx > best_idx:
					if target_idx > curr_idx:
						if next_idx <= target_idx:
							best_idx = next_idx
							best_dir = try_d
					else:
						best_idx = next_idx
						best_dir = try_d
			if best_dir != None:
				quick_print("shortcut to idx=" + str(best_idx))
				if move(best_dir):
					tail.append((x, y))
					while len(tail) > apples:
						tail.pop(0)
					moved = True
					quick_print("SHORTCUT OK")
		if not moved:
			next_cycle_idx = curr_idx + 1
			if next_cycle_idx < total:
				nx, ny = path[next_cycle_idx]
				d = get_dir_to(x, y, nx, ny)
				if d != None:
					if move(d):
						tail.append((x, y))
						while len(tail) > apples:
							tail.pop(0)
						moved = True
						quick_print("CYCLE OK")
		if not moved:
			tail_set = {}
			for pos in tail:
				tail_set[pos] = True
			for try_d in [North, East, South, West]:
				if try_d == North:
					nx, ny = x, y + 1
				elif try_d == South:
					nx, ny = x, y - 1
				elif try_d == East:
					nx, ny = x + 1, y
				else:
					nx, ny = x - 1, y
				if nx < 0 or nx >= size or ny < 0 or ny >= size:
					continue
				if (nx, ny) in tail_set:
					continue
				quick_print("fallback to (" + str(nx) + "," + str(ny) + ")")
				if move(try_d):
					tail.append((x, y))
					while len(tail) > apples:
						tail.pop(0)
					moved = True
					quick_print("FALLBACK OK")
					break
		if not moved:
			quick_print("STUCK")
			break
		move_count = move_count + 1
		if move_count > total * 2:
			quick_print("TOO MANY MOVES")
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
