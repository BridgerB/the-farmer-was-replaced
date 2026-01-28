TARGET = 10000000

clear()

start = get_time()
size = get_world_size()

quick_print("=== CACTUS OPTIMIZED ===")

def till_and_plant():
	for row in range(size):
		if get_ground_type() != Grounds.Soil:
			till()
		harvest()
		plant(Entities.Cactus)
		move(North)

def wait_column():
	for row in range(size):
		while get_entity_type() == Entities.Cactus and not can_harvest():
			pass
		move(North)

def sort_my_row():
	swapped = True
	while swapped:
		swapped = False
		while get_pos_x() != 0:
			move(West)
		for x in range(size - 1):
			if get_entity_type() == Entities.Cactus:
				left = measure()
				right = measure(East)
				if right != None and left > right:
					swap(East)
					swapped = True
			move(East)

def sort_my_col():
	swapped = True
	while swapped:
		swapped = False
		while get_pos_y() != 0:
			move(South)
		for y in range(size - 1):
			if get_entity_type() == Entities.Cactus:
				bottom = measure()
				top = measure(North)
				if top != None and bottom > top:
					swap(North)
					swapped = True
			move(North)

for col in range(size - 1):
	spawn_drone(till_and_plant)
	move(East)
till_and_plant()
while num_drones() > 1:
	pass

while get_pos_x() != 0:
	move(West)
for col in range(size - 1):
	spawn_drone(wait_column)
	move(East)
wait_column()
while num_drones() > 1:
	pass

while get_pos_x() != 0:
	move(West)
while get_pos_y() != 0:
	move(South)
for row in range(size - 1):
	spawn_drone(sort_my_row)
	move(North)
sort_my_row()
while num_drones() > 1:
	pass

while get_pos_x() != 0:
	move(West)
while get_pos_y() != 0:
	move(South)
for col in range(size - 1):
	spawn_drone(sort_my_col)
	move(East)
sort_my_col()
while num_drones() > 1:
	pass

while get_pos_x() != 0:
	move(West)
while get_pos_y() != 0:
	move(South)

harvest()

quick_print("Cactus: " + str(num_items(Items.Cactus)))
quick_print("Done: " + str(get_time() - start) + "s")
