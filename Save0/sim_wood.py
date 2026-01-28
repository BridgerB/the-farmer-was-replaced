TARGET = 10000000

clear()

def worker():
	while num_items(Items.Wood) < TARGET:
		entity = get_entity_type()
		if entity == Entities.Tree or entity == Entities.Bush:
			if can_harvest():
				harvest()
		else:
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
spawn_drone(worker)
for c in range(size - 2):
	move(East)
	spawn_drone(worker)
move(East)
while num_items(Items.Wood) < TARGET:
	entity = get_entity_type()
	if entity == Entities.Tree or entity == Entities.Bush:
		if can_harvest():
			harvest()
	else:
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
