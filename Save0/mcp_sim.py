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

def farm_zone(x_start, x_end, y_start, y_end):
	nav.go_to(x_start, y_start)
	height = y_end - y_start - 1
	for col in range(x_start, x_end):
		if (col - x_start) % 2 == 0:
			traverse_column_up(height)
		else:
			traverse_column_down(height)
		if col < x_end - 1:
			move(East)

def make_worker(x_start, x_end, y_start, y_end):
	def worker():
		farm_zone(x_start, x_end, y_start, y_end)
	return worker

start = get_time()
while num_items(Items.Hay) < 10000000:
	drone.run_parallel(make_worker, farm_zone)
elapsed = get_time() - start
quick_print("Hay: " + str(num_items(Items.Hay)))
quick_print("Time to 10M: " + str(elapsed) + "s")
