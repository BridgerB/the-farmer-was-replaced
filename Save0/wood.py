import nav
import drone
import logs

def farm_cell(x, y):
	if can_harvest():
		harvest()
	if get_entity_type() == None:
		if (x + y) % 2 == 0:
			plant(Entities.Tree)
		else:
			plant(Entities.Bush)

def farm_zone(x_start, x_end, y_start, y_end):
	nav.traverse_zone(x_start, x_end, y_start, y_end, farm_cell)

def make_worker(x_start, x_end, y_start, y_end):
	def worker():
		farm_zone(x_start, x_end, y_start, y_end)
	return worker

def cycle():
	logs.log("wood cycle")
	drone.run_parallel(make_worker, farm_zone)
