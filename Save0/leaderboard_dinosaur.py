# -----------------------------------------------------------------------------
# Leaderboards.Dinosaur entry point.
#
# Started via leaderboard_run(Leaderboards.Dinosaur, "leaderboard_dinosaur", speedup).
# Fixed starting conditions per docs/unlocks/leaderboard.md: everything
# unlocked, 1e9 Cactus and 1e9 Power. Goal: farm 33,488,928 bone (= filling
# a 32x32 area with the dinosaur tail) as fast as possible, then TERMINATE.
#
# Adapted from hamiltonian.py's proven never-self-traps chase, forced to
# size 32 to match what the target amount is actually calibrated for (see
# leaderboard_maze.py's world_size fix - same issue applies here: full
# unlocks default get_world_size() to the max, not 32).
# -----------------------------------------------------------------------------
import logs
import nav

def get_dir_to(my_x, my_y, target_x, target_y):
	dirs = []
	dx = target_x - my_x
	dy = target_y - my_y
	if dx > 0:
		dirs.append(East)
	if dx < 0:
		dirs.append(West)
	if dy > 0:
		dirs.append(North)
	if dy < 0:
		dirs.append(South)
	return dirs

def run_once():
	nav.go_to(0, 0)
	if get_entity_type() != None:
		harvest()
	change_hat(Hats.Dinosaur_Hat)
	tail = []
	apples = 0
	apple_x = -1
	apple_y = -1
	while True:
		my_x = get_pos_x()
		my_y = get_pos_y()
		if get_entity_type() == Entities.Apple:
			apples = apples + 1
			info = measure()
			if info != None:
				apple_x = info[0]
				apple_y = info[1]
			else:
				apple_x = -1
				apple_y = -1
		if apple_x >= 0:
			dirs_to_apple = get_dir_to(my_x, my_y, apple_x, apple_y)
		else:
			dirs_to_apple = []
		if len(tail) > 0:
			tail_x = tail[len(tail) - 1][0]
			tail_y = tail[len(tail) - 1][1]
			dirs_to_tail = get_dir_to(my_x, my_y, tail_x, tail_y)
		else:
			dirs_to_tail = []
		all_dirs = []
		for d in dirs_to_apple:
			all_dirs.append(d)
		for d in dirs_to_tail:
			if d not in all_dirs:
				all_dirs.append(d)
		for d in [North, East, South, West]:
			if d not in all_dirs:
				all_dirs.append(d)
		moved = False
		for d in all_dirs:
			if move(d):
				moved = True
				break
		if not moved:
			break
		tail.insert(0, (my_x, my_y))
		while len(tail) > apples:
			tail.pop()
	change_hat(Hats.Straw_Hat)

set_world_size(32)
GOAL = 33488928
while num_items(Items.Bone) < GOAL:
	run_once()
	logs.log("leaderboard dinosaur: bone=" + str(num_items(Items.Bone)))

logs.log("leaderboard dinosaur run complete: " + str(num_items(Items.Bone)))
