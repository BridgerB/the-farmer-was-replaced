import nav
import drone
import logs

def plant_and_measure(start_col, end_col):
	size = get_world_size()
	sunflowers = []
	for pos in nav.s_shape_range(start_col, end_col, size):
		nav.go_to(pos[0], pos[1])
		if get_ground_type() != Grounds.Soil:
			till()
		entity = get_entity_type()
		if entity != None and entity != Entities.Sunflower:
			harvest()
		if get_entity_type() == None and num_items(Items.Carrot) > 0:
			plant(Entities.Sunflower)
		if get_entity_type() == Entities.Sunflower:
			sunflowers.append([pos[0], pos[1], measure()])
	return sunflowers

def wait_for_ready(sunflowers):
	not_ready = sunflowers[:]
	while len(not_ready) > 0:
		still_waiting = []
		for sf in not_ready:
			nav.go_to(sf[0], sf[1])
			if get_entity_type() == Entities.Sunflower and not can_harvest():
				still_waiting.append(sf)
		not_ready = still_waiting

def harvest_petals(start_x, start_y, target):
	size = get_world_size()
	found = True
	while found:
		found = False
		for i in range(size * size):
			x = (start_x + i // size) % size
			y = (start_y + i % size) % size
			nav.go_to(x, y)
			if get_entity_type() == Entities.Sunflower:
				if measure() == target and can_harvest():
					harvest()
					found = True

def make_plant_worker(start_col, end_col):
	def worker():
		sfs = plant_and_measure(start_col, end_col)
		wait_for_ready(sfs)
	return worker

def make_harvest_worker(start_x, start_y, target):
	def worker():
		harvest_petals(start_x, start_y, target)
	return worker

def spawn_plant_workers():
	zones = drone.get_zone_bounds()
	for i in range(1, len(zones)):
		spawn_drone(make_plant_worker(zones[i][0], zones[i][1]))

def spawn_harvest_workers(target):
	size = get_world_size()
	starts = [[size - 1, 0], [0, size - 1], [size - 1, size - 1]]
	zones = drone.get_zone_bounds()
	for i in range(1, len(zones)):
		if i - 1 < len(starts):
			spawn_drone(make_harvest_worker(starts[i-1][0], starts[i-1][1], target))

def cycle():
	logs.log("sunflower cycle")
	drone.wait_for_workers()
	spawn_plant_workers()
	zone = drone.get_main_zone()
	my_sfs = plant_and_measure(zone[0], zone[1])
	wait_for_ready(my_sfs)
	drone.wait_for_workers()

	for target in range(15, 6, -1):
		spawn_harvest_workers(target)
		harvest_petals(0, 0, target)
		drone.wait_for_workers()
