TARGET = 10000000

clear()

start = get_time()
size = get_world_size()

quick_print("=== PUMPKIN BASELINE ===")
quick_print("Grid: " + str(size) + "x" + str(size) + " = " + str(size*size) + " cells")
quick_print("Max yield if all connected: " + str((size*size)*(size*size)*(size*size)))

def plant_column():
	for row in range(size):
		if get_ground_type() != Grounds.Soil:
			till()
		if get_water() < 0.8:
			use_item(Items.Water)
		plant(Entities.Pumpkin)
		move(North)

quick_print("Phase 1: Planting...")
plant_start = get_time()
for col in range(size - 1):
	spawn_drone(plant_column)
	move(East)
plant_column()
while num_drones() > 1:
	pass
quick_print("Plant done: " + str(get_time() - plant_start) + "s")

while get_pos_x() != 0:
	move(West)

def wait_column():
	for row in range(size):
		entity = get_entity_type()
		if entity == Entities.Pumpkin:
			while not can_harvest():
				if get_entity_type() != Entities.Pumpkin:
					break
		if get_entity_type() != Entities.Pumpkin:
			if get_water() < 0.8:
				use_item(Items.Water)
			plant(Entities.Pumpkin)
		move(North)

quick_print("Phase 2: Wait and replant...")
wait_start = get_time()
rounds = 0
all_ready = False

while not all_ready:
	rounds = rounds + 1
	for col in range(size - 1):
		spawn_drone(wait_column)
		move(East)
	wait_column()
	while num_drones() > 1:
		pass
	while get_pos_x() != 0:
		move(West)
	
	all_ready = True
	for x in range(size):
		for y in range(size):
			e = get_entity_type()
			if e != Entities.Pumpkin or not can_harvest():
				all_ready = False
			move(North)
		move(East)
	while get_pos_x() != 0:
		move(West)
	
	quick_print("Round " + str(rounds) + " complete")

quick_print("Wait done: " + str(get_time() - wait_start) + "s")

quick_print("Phase 3: Harvest...")
harvest()

quick_print("=== RESULTS ===")
quick_print("Pumpkins: " + str(num_items(Items.Pumpkin)))
quick_print("Total time: " + str(get_time() - start) + "s")
