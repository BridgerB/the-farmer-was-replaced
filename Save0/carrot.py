import movement

def can_afford(entity):
	cost = get_cost(entity)
	for item in cost:
		if num_items(item) < cost[item]:
			return False
	return True

def farm_cycle():
	size = get_world_size()
	total = size * size

	# Early exit if we can't afford carrots
	if not can_afford(Entities.Carrot):
		return

	movement.go_to_start()

	for i in range(total):
		# Check each tile - if we run out, exit early
		if not can_afford(Entities.Carrot):
			return

		# Harvest if ready
		if can_harvest():
			harvest()

		# Ensure soil
		if get_ground_type() != Grounds.Soil:
			till()

		# Plant carrot
		plant(Entities.Carrot)

		movement.move_next()

def farm_carrot():
	while True:
		farm_cycle()

if __name__ == "__main__":
	farm_carrot()
