def has_hay():
	return num_items(Items.Hay) > 0

def has_wood():
	return num_items(Items.Wood) > 0

def has_carrot():
	return num_items(Items.Carrot) > 0

def has_power():
	return num_items(Items.Power) > 0

POWER_THRESHOLD = 100
CARROT_MIN = 100
SUBSTANCE_MIN = 100

def get_weighted_resources():
	hay = num_items(Items.Hay)
	wood = num_items(Items.Wood)
	carrot = num_items(Items.Carrot)
	pumpkin = num_items(Items.Pumpkin)
	power = num_items(Items.Power)
	gold = num_items(Items.Gold)
	cactus = num_items(Items.Cactus)
	substance = num_items(Items.Weird_Substance)
	res = [
		["hay", hay],
		["wood", wood],
		["carrot", carrot],
		["pumpkin", pumpkin],
		["power", power],
		["gold", gold],
		["cactus", cactus],
		["substance", substance]
	]
	return res

def get_lowest_resource():
	res = get_weighted_resources()
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
	power = num_items(Items.Power)
	if power < POWER_THRESHOLD:
		return "power"
	carrot = num_items(Items.Carrot)
	if carrot < CARROT_MIN:
		return "carrot"
	size = get_world_size()
	substance_needed = size * (2 ** max(0, num_unlocked(Unlocks.Mazes) - 1))
	substance = num_items(Items.Weird_Substance)
	if substance < substance_needed and substance < SUBSTANCE_MIN:
		return "substance"
	return get_lowest_resource()
