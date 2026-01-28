TARGET = 10000000

def farm_cell():
	if get_ground_type() == Grounds.Soil:
		till()
	
	entity = get_entity_type()
	if entity != None and entity != Entities.Grass:
		harvest()
	
	if get_entity_type() == Entities.Grass and can_harvest():
		harvest()
	
	if get_entity_type() == None:
		plant(Entities.Grass)
	
	if get_entity_type() == Entities.Grass and not can_harvest():
		if num_items(Items.Fertilizer) > 0:
			use_item(Items.Fertilizer)
		if can_harvest():
			harvest()

def farm_column_up():
	size = get_world_size()
	for row in range(size):
		farm_cell()
		if row < size - 1:
			move(North)

def farm_column_down():
	size = get_world_size()
	for row in range(size):
		farm_cell()
		if row > 0:
			move(South)

def make_worker(col, going_up):
	def worker():
		size = get_world_size()
		while get_pos_x() < col:
			move(East)
		if going_up:
			while get_pos_y() > 0:
				move(South)
			farm_column_up()
		else:
			while get_pos_y() < size - 1:
				move(North)
			farm_column_down()
	return worker

clear()
start = get_time()
size = get_world_size()

quick_print("=== WEIRD SIM (alternating - BEST) ===")

while get_pos_x() > 0:
	move(West)
while get_pos_y() > 0:
	move(South)

passes = 0
going_up = True

while num_items(Items.Weird_Substance) < TARGET:
	passes = passes + 1
	
	for col in range(1, size):
		spawn_drone(make_worker(col, going_up))
	
	if going_up:
		farm_column_up()
	else:
		farm_column_down()
	
	while num_drones() > 1:
		pass
	
	going_up = not going_up
	
	if passes <= 5 or passes % 10 == 0:
		quick_print("P" + str(passes) + ": " + str(num_items(Items.Weird_Substance)) + " @" + str(get_time() - start) + "s")

elapsed = get_time() - start
quick_print("Done: " + str(num_items(Items.Weird_Substance)) + " in " + str(elapsed) + "s (" + str(passes) + " passes)")
