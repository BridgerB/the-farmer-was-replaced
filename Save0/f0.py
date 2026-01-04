def farm_weird_substance():
	size = get_world_size()

	while True:
		for x in range(size):
			for y in range(size):
				# Go to position
				while get_pos_x() < x:
					move(East)
				while get_pos_x() > x:
					move(West)
				while get_pos_y() < y:
					move(North)
				while get_pos_y() > y:
					move(South)

				# Harvest if ready
				if can_harvest():
					harvest()

				# Need turf for grass
				if get_ground_type() == Grounds.Soil:
					till()

				# Plant grass (free)
				if get_entity_type() == None:
					plant(Entities.Grass)

				# Fertilize until grown (makes it infected)
				while not can_harvest() and get_entity_type() == Entities.Grass:
					if num_items(Items.Fertilizer) > 0:
						use_item(Items.Fertilizer)

if __name__ == "__main__":
	farm_weird_substance()
	