APPLES_NEEDED = 560

def go_home():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

def build_cycle_with_dirs(size):
	path = []
	dirs = []
	
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
	
	for i in range(len(path)):
		nx, ny = path[(i + 1) % len(path)]
		cx, cy = path[i]
		dx = nx - cx
		dy = ny - cy
		if dx > 0:
			dirs.append(East)
		elif dx < 0:
			dirs.append(West)
		elif dy > 0:
			dirs.append(North)
		else:
			dirs.append(South)
	
	return (path, dirs)

def chase(dirs, idx_map, target_apples):
	path_len = len(dirs)
	apples = 0
	moves = 0
	current_idx = idx_map[(get_pos_x(), get_pos_y())]
	
	while apples < target_apples:
		if get_entity_type() == Entities.Apple:
			apples = apples + 1
			measure()
		move(dirs[current_idx])
		moves = moves + 1
		current_idx = current_idx + 1
		if current_idx >= path_len:
			current_idx = 0
	
	return (apples, moves)

clear()
set_world_size(24)
start = get_time()
size = get_world_size()

path, dirs = build_cycle_with_dirs(size)
idx_map = {}
for i in range(len(path)):
	idx_map[path[i]] = i

quick_print("=== BONE SIM ===")

if get_entity_type() != None:
	harvest()

go_home()
change_hat(Hats.Dinosaur_Hat)

apples, moves = chase(dirs, idx_map, APPLES_NEEDED)

change_hat(Hats.Straw_Hat)
bones = num_items(Items.Bone)
elapsed = get_time() - start
quick_print(str(apples) + "a " + str(moves) + "m -> " + str(bones) + " bones in " + str(elapsed) + "s")
