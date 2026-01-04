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

def farm_zone(start_col, end_col):
	nav.traverse_zone(start_col, end_col, farm_cell)

def make_worker(start_col, end_col):
	def worker():
		farm_zone(start_col, end_col)
	return worker

def cycle():
	logs.log("wood cycle")
	drone.run_parallel(make_worker, farm_zone)
