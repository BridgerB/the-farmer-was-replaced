import nav
import drone

def farm_cell(x, y):
	if can_harvest():
		harvest()
	if get_entity_type() == None:
		plant(Entities.Grass)

def farm_zone(x_start, x_end, y_start, y_end):
	nav.traverse_zone(x_start, x_end, y_start, y_end, farm_cell)

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
