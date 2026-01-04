import movement

def process_tile():
	# Harvest if ready
	if can_harvest():
		harvest()

	# If soil, till to convert back to turf for grass
	if get_ground_type() == Grounds.Soil:
		till()

	# Plant grass if empty
	if get_entity_type() == None:
		plant(Entities.Grass)

def farm_cycle():
	movement.traverse_all(process_tile)

def farm_hay():
	while True:
		farm_cycle()

if __name__ == "__main__":
	farm_hay()
