TARGET = 10000000

clear()

start = get_time()
size = get_world_size()

def plant_checkerboard():
	x = get_pos_x()
	for row in range(size):
		y = get_pos_y()
		if (x + y) % 2 == 0:
			till()
			use_item(Items.Water)
			plant(Entities.Carrot)
		else:
			plant(Entities.Bush)
		move(North)

for col in range(size - 1):
	spawn_drone(plant_checkerboard)
	move(East)
plant_checkerboard()

while num_drones() > 1:
	pass

while get_pos_x() != 0:
	move(West)
while get_pos_y() != 0:
	move(South)

while not can_harvest():
	pass

def harvest_all():
	x = get_pos_x()
	while num_items(Items.Carrot) < TARGET:
		harvest()
		plant(Entities.Carrot)
		move(North)

for col in range(size - 1):
	spawn_drone(harvest_all)
	move(East)
harvest_all()

while num_drones() > 1:
	pass

quick_print("Carrots: " + str(num_items(Items.Carrot)))
quick_print("Total: " + str(get_time() - start) + "s")
