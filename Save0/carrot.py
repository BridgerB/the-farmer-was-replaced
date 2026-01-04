import nav
import drone
import logs

def farm_cell(x, y):
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() == None:
		plant(Entities.Carrot)
		return
	if can_harvest():
		harvest()
		plant(Entities.Carrot)

def farm_zone(start_col, end_col):
	nav.traverse_zone(start_col, end_col, farm_cell)

def make_worker(start_col, end_col):
	def worker():
		farm_zone(start_col, end_col)
	return worker

def cycle():
	logs.log("carrot cycle")
	drone.run_parallel(make_worker, farm_zone)
