TARGET = 10000000
MAX_APPLES = 254

def go_home():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

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
	return path

def get_dir(fx, fy, tx, ty):
	if tx > fx:
		return East
	if tx < fx:
		return West
	if ty > fy:
		return North
	return South

def chase(size, path, idx_map):
	path_len = len(path)
	apples = 0
	moves = 0
	
	mx = get_pos_x()
	my = get_pos_y()
	current_idx = idx_map[(mx, my)]
	
	while apples < MAX_APPLES and num_items(Items.Bone) < TARGET:
		if get_entity_type() == Entities.Apple:
			apples = apples + 1
			measure()
		
		next_idx = (current_idx + 1) % path_len
		nx, ny = path[next_idx]
		d = get_dir(mx, my, nx, ny)
		
		if not move(d):
			return (apples, moves, "blocked")
		
		moves = moves + 1
		mx, my = nx, ny
		current_idx = next_idx
	
	if num_items(Items.Bone) >= TARGET:
		return (apples, moves, "target")
	return (apples, moves, "full")

clear()
set_world_size(16)
start = get_time()
size = get_world_size()
path = build_cycle(size)
idx_map = {}
for i in range(len(path)):
	idx_map[path[i]] = i

quick_print("=== HAMILTONIAN BONE SIM ===")
quick_print("Grid: " + str(size) + " Max: " + str(MAX_APPLES) + " apples/cycle")

if get_entity_type() != None:
	harvest()

go_home()
change_hat(Hats.Dinosaur_Hat)

cycle = 0
while num_items(Items.Bone) < TARGET:
	cycle = cycle + 1
	apples, moves, reason = chase(size, path, idx_map)
	bones = num_items(Items.Bone)
	quick_print("C" + str(cycle) + ": " + str(apples) + "a " + str(moves) + "m " + reason + " -> " + str(bones))
	
	if reason == "blocked":
		quick_print("Unexpected block!")
		break
	
	if reason != "target":
		change_hat(Hats.Straw_Hat)
		if get_entity_type() != None:
			harvest()
		go_home()
		change_hat(Hats.Dinosaur_Hat)

change_hat(Hats.Straw_Hat)
elapsed = get_time() - start
quick_print("")
quick_print("Done: " + str(num_items(Items.Bone)) + " bones in " + str(elapsed) + "s")
