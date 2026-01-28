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

def farm_column(col):
	size = get_world_size()
	while get_pos_x() < col:
		move(East)
	while get_pos_x() > col:
		move(West)
	while get_pos_y() > 0:
		move(South)
	
	for row in range(size):
		farm_cell()
		if row < size - 1:
			move(North)

def make_worker(col):
	def worker():
		farm_column(col)
	return worker

def farm_pass_parallel():
	size = get_world_size()
	
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)
	
	for col in range(1, size):
		spawn_drone(make_worker(col))
	
	farm_column(0)
	
	while num_drones() > 1:
		pass

clear()
start = get_time()
size = get_world_size()

quick_print("=== WEIRD SUBSTANCE SIM (parallel) ===")
quick_print("Grid: " + str(size) + "x" + str(size))
quick_print("Drones: " + str(max_drones()))
quick_print("Starting fertilizer: " + str(num_items(Items.Fertilizer)))

passes = 0
start_substance = num_items(Items.Weird_Substance)
start_fertilizer = num_items(Items.Fertilizer)

while num_items(Items.Weird_Substance) < TARGET:
	passes = passes + 1
	pass_start_sub = num_items(Items.Weird_Substance)
	pass_start_fert = num_items(Items.Fertilizer)
	
	farm_pass_parallel()
	
	substance = num_items(Items.Weird_Substance)
	fertilizer = num_items(Items.Fertilizer)
	elapsed = get_time() - start
	
	sub_this_pass = substance - pass_start_sub
	fert_this_pass = pass_start_fert - fertilizer
	
	if passes <= 10 or passes % 10 == 0:
		quick_print("P" + str(passes) + ": +" + str(sub_this_pass) + " sub, total=" + str(substance) + " @" + str(elapsed) + "s")

elapsed = get_time() - start
substance_gained = num_items(Items.Weird_Substance) - start_substance
fertilizer_used = start_fertilizer - num_items(Items.Fertilizer)

quick_print("")
quick_print("=== RESULTS ===")
quick_print("Substance: " + str(substance_gained))
quick_print("Fertilizer used: " + str(fertilizer_used))
quick_print("Time: " + str(elapsed) + "s")
quick_print("Passes: " + str(passes))
