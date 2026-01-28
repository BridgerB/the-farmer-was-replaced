TARGET = 10000000

clear()

start = get_time()
size = get_world_size()
mid = size / 2

def plant_column():
	for row in range(size):
		if get_ground_type() != Grounds.Soil:
			till()
		use_item(Items.Water)
		plant(Entities.Pumpkin)
		move(North)

def replant_only():
	for row in range(size):
		if get_entity_type() != Entities.Pumpkin:
			use_item(Items.Water)
			plant(Entities.Pumpkin)
		move(North)

def wait_and_replant():
	for row in range(size):
		e = get_entity_type()
		if e == Entities.Pumpkin:
			while not can_harvest():
				if get_entity_type() != Entities.Pumpkin:
					break
		if get_entity_type() != Entities.Pumpkin:
			use_item(Items.Water)
			plant(Entities.Pumpkin)
		move(North)

harvests = 0

while num_items(Items.Pumpkin) < TARGET:
	harvests = harvests + 1
	
	for col in range(size - 1):
		spawn_drone(plant_column)
		move(East)
	plant_column()
	while num_drones() > 1:
		pass
	
	for col in range(size - 1):
		spawn_drone(replant_only)
		move(West)
	replant_only()
	while num_drones() > 1:
		pass
	
	for col in range(size - 1):
		spawn_drone(replant_only)
		move(East)
	replant_only()
	while num_drones() > 1:
		pass
	
	for col in range(size - 1):
		spawn_drone(wait_and_replant)
		move(West)
	wait_and_replant()
	while num_drones() > 1:
		pass
	
	while get_pos_x() < mid:
		move(East)
	while get_pos_y() < mid:
		move(North)
	
	harvest()
	quick_print("H" + str(harvests) + ": " + str(num_items(Items.Pumpkin)))

quick_print("Done: " + str(get_time() - start) + "s")
