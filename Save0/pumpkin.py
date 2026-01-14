import nav
import drone
import logs
import resources

def process_zone(x_start, x_end, y_start, y_end):
	pending = {}
	for pos in nav.s_shape_range(x_start, x_end, y_start, y_end):
		nav.go_to(pos[0], pos[1])
		if get_ground_type() != Grounds.Soil:
			till()
		if get_water() < 0.8 and num_items(Items.Water) > 0:
			use_item(Items.Water)
		entity = get_entity_type()
		if entity != Entities.Pumpkin:
			if entity != None and can_harvest():
				harvest()
			if num_items(Items.Carrot) > 0:
				plant(Entities.Pumpkin)
				pending[(pos[0], pos[1])] = True

	while len(pending) > 0:
		first_pos = None
		for p in pending:
			first_pos = p
			break
		nav.go_to(first_pos[0], first_pos[1])
		if get_entity_type() == Entities.Pumpkin:
			while not can_harvest():
				pass

		next_pending = {}
		for pos in pending:
			nav.go_to(pos[0], pos[1])
			entity = get_entity_type()
			if entity == None or entity == Entities.Dead_Pumpkin:
				if num_items(Items.Carrot) == 0:
					return
				if get_water() < 0.8 and num_items(Items.Water) > 0:
					use_item(Items.Water)
				plant(Entities.Pumpkin)
				next_pending[pos] = True
		pending = next_pending

def make_worker(x_start, x_end, y_start, y_end):
	def worker():
		process_zone(x_start, x_end, y_start, y_end)
	return worker

def cycle():
	logs.log("pumpkin cycle")
	if not resources.has_carrot():
		return
	drone.wait_for_workers()
	drone.spawn_zone_workers(make_worker)
	zone = drone.get_main_zone()
	process_zone(zone[0], zone[1], zone[2], zone[3])
	drone.wait_for_workers()
	harvest()
	nav.go_to(0, 0)
