def farm_cell():
	if can_harvest():
		harvest()
	if get_entity_type() == None:
		plant(Entities.Grass)

def cycle():
	size = get_world_size()
	for x in range(size):
		for y in range(size):
			move(North)
			farm_cell()
		move(East)

start = get_time()
while num_items(Items.Hay) < 1000000:
	cycle()
elapsed = get_time() - start
quick_print("Hay: " + str(num_items(Items.Hay)))
quick_print("Time to 1M: " + str(elapsed) + "s")
