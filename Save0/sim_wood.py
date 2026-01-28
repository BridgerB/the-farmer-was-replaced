TARGET = 10000000
clear()

def planter():
	for i in range(32):
		x = get_pos_x()
		y = get_pos_y()
		if (x + y) % 2 == 0:
			plant(Entities.Tree)
		else:
			plant(Entities.Bush)
		move(North)

def harvester():
	while num_items(Items.Wood) < TARGET:
		if can_harvest():
			harvest()
			x = get_pos_x()
			y = get_pos_y()
			if (x + y) % 2 == 0:
				plant(Entities.Tree)
			else:
				plant(Entities.Bush)
		move(North)

start = get_time()
size = get_world_size()

spawn_drone(planter)
for c in range(size - 2):
	move(East)
	spawn_drone(planter)
move(East)
for i in range(32):
	x = get_pos_x()
	y = get_pos_y()
	if (x + y) % 2 == 0:
		plant(Entities.Tree)
	else:
		plant(Entities.Bush)
	move(North)

while num_drones() > 1:
	pass

for c in range(size - 1):
	move(West)
	spawn_drone(harvester)
spawn_drone(harvester)

while num_items(Items.Wood) < TARGET:
	if can_harvest():
		harvest()
		x = get_pos_x()
		y = get_pos_y()
		if (x + y) % 2 == 0:
			plant(Entities.Tree)
		else:
			plant(Entities.Bush)
	move(North)

quick_print("Wood: " + str(num_items(Items.Wood)))
quick_print("Time to 10M: " + str(get_time() - start) + "s")
