TARGET = 10000000

clear()

def tiller_planter():
	for i in range(32):
		till()
		use_item(Items.Water)
		plant(Entities.Carrot)
		move(North)

def harvester():
	while num_items(Items.Carrot) < TARGET:
		harvest()
		if get_water() < 0.3:
			use_item(Items.Water)
		plant(Entities.Carrot)
		move(North)

start = get_time()
size = get_world_size()

spawn_drone(tiller_planter)
for c in range(size - 2):
	move(East)
	spawn_drone(tiller_planter)
move(East)
for i in range(32):
	till()
	use_item(Items.Water)
	plant(Entities.Carrot)
	move(North)

while num_drones() > 1:
	pass

for c in range(size - 1):
	move(West)
	spawn_drone(harvester)
spawn_drone(harvester)

while num_items(Items.Carrot) < TARGET:
	harvest()
	if get_water() < 0.3:
		use_item(Items.Water)
	plant(Entities.Carrot)
	move(North)

quick_print("Carrot: " + str(num_items(Items.Carrot)))
quick_print("Time to 10M: " + str(get_time() - start) + "s")
