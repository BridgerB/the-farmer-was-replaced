import nav
import drone
import logs

def farm_cell(x, y):
	if can_harvest():
		harvest()
	if get_ground_type() == Grounds.Soil:
		till()
	if get_entity_type() == None:
		plant(Entities.Grass)
	if get_entity_type() == Entities.Grass and not can_harvest():
		if num_items(Items.Fertilizer) > 0:
			use_item(Items.Fertilizer)

def farm_zone(x_start, x_end, y_start, y_end):
	nav.traverse_zone(x_start, x_end, y_start, y_end, farm_cell)

def make_worker(x_start, x_end, y_start, y_end):
	def worker():
		farm_zone(x_start, x_end, y_start, y_end)
	return worker

def cycle():
	logs.log("substance cycle")
	drone.run_parallel(make_worker, farm_zone)
