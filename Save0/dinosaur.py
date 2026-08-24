import logs

def get_next_position(x, y, direction):
	if direction == North:
		return (x, y + 1)
	if direction == South:
		return (x, y - 1)
	if direction == East:
		return (x + 1, y)
	return (x - 1, y)

def build_cycle(size):
	path = []
	for row in range(size):
		path.append((0, row))
	for col in range(1, size):
		if col % 2 == 1:
			for row in range(size - 1, 0, -1):
				path.append((col, row))
		else:
			for row in range(1, size):
				path.append((col, row))
	for col in range(size - 1, 0, -1):
		path.append((col, 0))
	idx_map = {}
	for i in range(len(path)):
		idx_map[path[i]] = i
	return idx_map

def go_home():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

def chase_apples_hamiltonian(idx_map, n):
	apples = 0
	moves = 0
	tail = []
	apple_idx = -1
	max_moves = n * 20

	while moves < max_moves:
		hx = get_pos_x()
		hy = get_pos_y()

		if get_entity_type() == Entities.Apple:
			apples = apples + 1
			info = measure()
			if info != None:
				apple_idx = idx_map[(info[0], info[1])]
			if apples % 50 == 0:
				logs.log("apples=" + str(apples))

		head_idx = idx_map[(hx, hy)]

		# Tightest constraint = closest tail segment in cycle order, not just
		# the oldest one. Shortcuts mean the tail is no longer a contiguous
		# cyclic range behind head, so checking only the oldest segment can
		# let a "safe" shortcut jump straight over a middle segment.
		min_tail_gap = n - 1
		for seg in tail:
			seg_idx = idx_map[seg]
			gap = (seg_idx - head_idx) % n
			if gap < min_tail_gap:
				min_tail_gap = gap

		best_dir = None
		best_remaining = n + 1
		for d in [North, East, South, West]:
			nx, ny = get_next_position(hx, hy, d)
			if (nx, ny) not in idx_map:
				continue
			blocked = False
			for i in range(len(tail) - 1):
				if tail[i][0] == nx and tail[i][1] == ny:
					blocked = True
					break
			if blocked:
				continue
			cand_idx = idx_map[(nx, ny)]
			fwd_gap = (cand_idx - head_idx) % n
			if fwd_gap == 0 or fwd_gap >= min_tail_gap:
				continue
			if apple_idx >= 0:
				remaining = (apple_idx - cand_idx) % n
			else:
				remaining = fwd_gap
			if remaining < best_remaining:
				best_remaining = remaining
				best_dir = d

		if best_dir == None:
			logs.log("STUCK at " + str(hx) + "," + str(hy) + " apples=" + str(apples))
			return apples

		if not move(best_dir):
			logs.log("MOVE FAILED at " + str(hx) + "," + str(hy) + " apples=" + str(apples))
			return apples

		tail.insert(0, (hx, hy))
		while len(tail) > apples:
			tail.pop()
		moves = moves + 1

	return apples

def cycle():
	logs.log("Starting dinosaur")
	if num_items(Items.Cactus) < 100:
		return True
	go_home()
	if get_entity_type() != None:
		harvest()
	size = get_world_size()
	idx_map = build_cycle(size)
	n = len(idx_map)
	change_hat(Hats.Dinosaur_Hat)
	apples = chase_apples_hamiltonian(idx_map, n)
	change_hat(Hats.Straw_Hat)
	logs.log("Dinosaur done: " + str(apples) + " apples -> " + str(apples * apples) + " bones")
	return True
