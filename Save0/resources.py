def has_hay():
	return num_items(Items.Hay) > 0

def has_wood():
	return num_items(Items.Wood) > 0

def has_carrot():
	return num_items(Items.Carrot) > 0

def get_lowest_resource():
	res = [
		["hay", num_items(Items.Hay)],
		["wood", num_items(Items.Wood)],
		["carrot", num_items(Items.Carrot)],
		["pumpkin", num_items(Items.Pumpkin)],
		["power", num_items(Items.Power)],
		["gold", num_items(Items.Gold)]
	]
	lowest = res[0]
	for r in res:
		if r[1] < lowest[1]:
			lowest = r
	return lowest[0]

def get_next_crop():
	if not has_hay():
		return "hay"
	if not has_wood():
		return "wood"
	if not has_carrot():
		return "carrot"
	return get_lowest_resource()
