import nav
import drone
import logs

first_planted = None

def plant_zone(x_start, x_end, y_start, y_end):
	global first_planted
	for pos in nav.s_shape_range(x_start, x_end, y_start, y_end):
		nav.go_to(pos[0], pos[1])
		if get_ground_type() != Grounds.Soil:
			till()
		if get_water() < 0.8 and num_items(Items.Water) > 0:
			use_item(Items.Water)
		entity = get_entity_type()
		if entity != None and entity != Entities.Sunflower:
			harvest()
		if get_entity_type() == None and num_items(Items.Carrot) > 0:
			plant(Entities.Sunflower)
			if first_planted == None:
				first_planted = (pos[0], pos[1])

def make_plant_worker(x_start, x_end, y_start, y_end):
	def worker():
		plant_zone(x_start, x_end, y_start, y_end)
	return worker

def harvest_zone_petal(x_start, x_end, y_start, y_end, target):
	for pos in nav.s_shape_range(x_start, x_end, y_start, y_end):
		nav.go_to(pos[0], pos[1])
		if get_entity_type() == Entities.Sunflower:
			if measure() == target and can_harvest():
				harvest()

def make_petal_worker(x_start, x_end, y_start, y_end, target):
	def worker():
		harvest_zone_petal(x_start, x_end, y_start, y_end, target)
	return worker

def cycle():
	global first_planted
	logs.log("sunflower cycle")
	first_planted = None
	drone.wait_for_workers()
	drone.spawn_zone_workers(make_plant_worker)
	zone = drone.get_main_zone()
	plant_zone(zone[0], zone[1], zone[2], zone[3])
	drone.wait_for_workers()
	if first_planted != None:
		nav.go_to(first_planted[0], first_planted[1])
		while get_entity_type() == Entities.Sunflower and not can_harvest():
			pass
	zones = drone.get_zone_bounds()
	for target in range(15, 6, -1):
		for i in range(1, len(zones)):
			spawn_drone(make_petal_worker(zones[i][0], zones[i][1], zones[i][2], zones[i][3], target))
		harvest_zone_petal(zone[0], zone[1], zone[2], zone[3], target)
		drone.wait_for_workers()
