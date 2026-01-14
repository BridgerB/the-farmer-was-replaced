import nav

companion_map = {}

def clear_companions():
	global companion_map
	companion_map = {}

def register_companion(plant_pos, companion_type, companion_pos):
	global companion_map
	key = (companion_pos[0], companion_pos[1])
	if key not in companion_map:
		companion_map[key] = []
	companion_map[key].append({
		"plant": plant_pos,
		"type": companion_type
	})

def check_and_plant_after(x, y):
	companion = get_companion()
	if companion == None:
		return
	comp_type = companion[0]
	comp_pos = companion[1]
	register_companion((x, y), comp_type, comp_pos)

def fulfill_companions_for_type(entity_type):
	global companion_map
	fulfilled = []
	for pos in companion_map:
		entries = companion_map[pos]
		for entry in entries:
			if entry["type"] == entity_type:
				fulfilled.append(pos)
				break
	for pos in fulfilled:
		nav.go_to(pos[0], pos[1])
		entity = get_entity_type()
		if entity != entity_type:
			if entity != None:
				if can_harvest():
					harvest()
				else:
					continue
			if entity_type == Entities.Grass:
				plant(Entities.Grass)
			elif entity_type == Entities.Bush:
				plant(Entities.Bush)
			elif entity_type == Entities.Tree:
				if num_items(Items.Wood) > 0:
					plant(Entities.Tree)
			elif entity_type == Entities.Carrot:
				if get_ground_type() != Grounds.Soil:
					till()
				if num_items(Items.Carrot) > 0:
					plant(Entities.Carrot)

def get_needed_companion_types():
	global companion_map
	types = {}
	for pos in companion_map:
		for entry in companion_map[pos]:
			types[entry["type"]] = True
	result = []
	for t in types:
		result.append(t)
	return result
	