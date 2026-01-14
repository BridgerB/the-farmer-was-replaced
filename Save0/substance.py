import nav
import drone
import logs

def farm_cell(x, y):
	if get_ground_type() == Grounds.Soil:
		till()
	entity = get_entity_type()
	if entity == Entities.Grass:
		if can_harvest():
			harvest()
			plant(Entities.Grass)
		elif num_items(Items.Fertilizer) > 0:
			use_item(Items.Fertilizer)
	elif entity == None:
		plant(Entities.Grass)
	else:
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

def cycle():
	logs.log("substance cycle")
	drone.run_parallel(make_worker, farm_zone)
