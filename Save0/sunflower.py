import nav
import drone
import logs

def plant_zone(start_col, end_col):
	size = get_world_size()
	for pos in nav.s_shape_range(start_col, end_col, size):
		nav.go_to(pos[0], pos[1])
		if get_ground_type() != Grounds.Soil:
			till()
		entity = get_entity_type()
		if entity != None and entity != Entities.Sunflower:
			harvest()
		if get_entity_type() == None and num_items(Items.Carrot) > 0:
			plant(Entities.Sunflower)

def make_plant_worker(start_col, end_col):
	def worker():
		plant_zone(start_col, end_col)
	return worker

def scan_field():
	size = get_world_size()
	petal_map = {}
	for i in range(7, 16):
		petal_map[i] = []
	for pos in nav.s_shape_range(0, size, size):
		nav.go_to(pos[0], pos[1])
		if get_entity_type() == Entities.Sunflower:
			petals = measure()
			petal_map[petals].append((pos[0], pos[1]))
	return petal_map

def wait_for_ready(petal_map):
	for petals in petal_map:
		if len(petal_map[petals]) > 0:
			pos = petal_map[petals][0]
			nav.go_to(pos[0], pos[1])
			while not can_harvest():
				pass
			return

def make_harvest_worker(positions):
	def worker():
		for pos in positions:
			nav.go_to(pos[0], pos[1])
			if get_entity_type() == Entities.Sunflower:
				if can_harvest():
					harvest()
	return worker

def harvest_petal_parallel(positions):
	if len(positions) == 0:
		return
	total = max_drones()
	chunk = max(1, (len(positions) + total - 1) // total)
	for i in range(1, total):
		start = i * chunk
		end = min(start + chunk, len(positions))
		if start < len(positions):
			spawn_drone(make_harvest_worker(positions[start:end]))
	for pos in positions[0:chunk]:
		nav.go_to(pos[0], pos[1])
		if get_entity_type() == Entities.Sunflower:
			if can_harvest():
				harvest()
	drone.wait_for_workers()

def cycle():
	logs.log("sunflower cycle")
	drone.wait_for_workers()
	drone.spawn_zone_workers(make_plant_worker)
	zone = drone.get_main_zone()
	plant_zone(zone[0], zone[1])
	drone.wait_for_workers()
	petal_map = scan_field()
	wait_for_ready(petal_map)
	for target in range(15, 6, -1):
		harvest_petal_parallel(petal_map[target])
