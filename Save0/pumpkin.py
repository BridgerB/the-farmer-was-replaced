import nav
import drone
import logs
import resources

def plant_cell(x, y):
	nav.go_to(x, y)
	if get_ground_type() != Grounds.Soil:
		till()
	if get_water() < 0.8 and num_items(Items.Water) > 0:
		use_item(Items.Water)
	entity = get_entity_type()
	if entity == Entities.Pumpkin:
		return
	if entity != None and can_harvest():
		harvest()
	if num_items(Items.Carrot) > 0:
		plant(Entities.Pumpkin)

def verify_zone(start_col, end_col):
	size = get_world_size()
	positions = nav.s_shape_range(start_col, end_col, size)

	for pos in positions:
		plant_cell(pos[0], pos[1])

	not_ready = []
	for pos in positions:
		nav.go_to(pos[0], pos[1])
		if get_entity_type() == Entities.Pumpkin:
			if not can_harvest():
				not_ready.append(pos)
		elif get_entity_type() == None and num_items(Items.Carrot) > 0:
			plant(Entities.Pumpkin)
			not_ready.append(pos)

	while len(not_ready) > 0:
		still_waiting = []
		for pos in not_ready:
			nav.go_to(pos[0], pos[1])
			if get_entity_type() == Entities.Pumpkin and not can_harvest():
				still_waiting.append(pos)
			elif get_entity_type() == None and num_items(Items.Carrot) > 0:
				plant(Entities.Pumpkin)
				still_waiting.append(pos)
		not_ready = still_waiting

def make_worker(start_col, end_col):
	def worker():
		verify_zone(start_col, end_col)
	return worker

def cycle():
	logs.log("pumpkin cycle")
	if not resources.has_carrot():
		return
	drone.wait_for_workers()
	drone.spawn_zone_workers(make_worker)
	zone = drone.get_main_zone()
	verify_zone(zone[0], zone[1])
	drone.wait_for_workers()
	harvest()
	nav.go_to(0, 0)
