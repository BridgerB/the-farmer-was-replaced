import nav
import drone
import logs
import poly

def farm_cell(x, y):
	if get_ground_type() != Grounds.Soil:
		till()
	if get_water() < 0.8 and num_items(Items.Water) > 0:
		use_item(Items.Water)
	entity = get_entity_type()
	if entity == None:
		if num_items(Items.Carrot) > 0:
			plant(Entities.Carrot)
			poly.check_and_plant_after(x, y)
		return
	if entity == Entities.Carrot:
		if can_harvest():
			harvest()
			if num_items(Items.Carrot) > 0:
				plant(Entities.Carrot)
				poly.check_and_plant_after(x, y)
		return
	if can_harvest():
		harvest()
	if get_entity_type() == None and num_items(Items.Carrot) > 0:
		plant(Entities.Carrot)
		poly.check_and_plant_after(x, y)

def farm_zone(x_start, x_end, y_start, y_end):
	nav.traverse_zone(x_start, x_end, y_start, y_end, farm_cell)

def make_worker(x_start, x_end, y_start, y_end):
	def worker():
		farm_zone(x_start, x_end, y_start, y_end)
	return worker

def cycle():
	logs.log("carrot cycle")
	poly.clear_companions()
	drone.run_parallel(make_worker, farm_zone)
	needed = poly.get_needed_companion_types()
	for comp_type in needed:
		poly.fulfill_companions_for_type(comp_type)
