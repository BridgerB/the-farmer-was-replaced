import nav
import drone
import logs
import resources

def plant_all():
	size = get_world_size()
	for pos in nav.s_shape_range(0, size, 0, size):
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

def wait_and_replant():
	size = get_world_size()
	all_ready = False
	while not all_ready:
		all_ready = True
		for pos in nav.s_shape_range(0, size, 0, size):
			nav.go_to(pos[0], pos[1])
			entity = get_entity_type()
			if entity == Entities.Pumpkin:
				if not can_harvest():
					all_ready = False
					while not can_harvest():
						if get_entity_type() != Entities.Pumpkin:
							break
			elif entity == Entities.Dead_Pumpkin or entity == None:
				all_ready = False
				if num_items(Items.Carrot) == 0:
					return False
				if get_water() < 0.8 and num_items(Items.Water) > 0:
					use_item(Items.Water)
				plant(Entities.Pumpkin)
	return True

def cycle():
	logs.log("pumpkin cycle")
	if not resources.has_carrot():
		return
	drone.wait_for_workers()
	plant_all()
	success = wait_and_replant()
	if success:
		nav.go_to(0, 0)
		harvest()
