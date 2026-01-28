import nav
import drone

def farm_cell():
	if can_harvest():
		harvest()

def traverse_column_up(height):
	for i in range(height):
		farm_cell()
		move(North)
	farm_cell()

def traverse_column_down(height):
	for i in range(height):
		farm_cell()
		move(South)
	farm_cell()

def farm_zone_once(x_start, x_end, y_start, y_end):
	height = y_end - y_start - 1
	for col in range(x_start, x_end):
		if (col - x_start) % 2 == 0:
			traverse_column_up(height)
		else:
			traverse_column_down(height)
		if col < x_end - 1:
			move(East)

def farm_zone_loop(x_start, x_end, y_start, y_end):
	nav.go_to(x_start, y_start)
	while num_items(Items.Hay) < 10000000:
		farm_zone_once(x_start, x_end, y_start, y_end)
		nav.go_to(x_start, y_start)

def make_worker(x_start, x_end, y_start, y_end):
	def worker():
		farm_zone_loop(x_start, x_end, y_start, y_end)
	return worker

start = get_time()
zones = drone.get_zone_bounds()
for i in range(1, len(zones)):
	z = zones[i]
	spawn_drone(make_worker(z[0], z[1], z[2], z[3]))
farm_zone_loop(zones[0][0], zones[0][1], zones[0][2], zones[0][3])
elapsed = get_time() - start
quick_print("Hay: " + str(num_items(Items.Hay)))
quick_print("Time to 10M: " + str(elapsed) + "s")
