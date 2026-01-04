def farm_cycle():
	size = get_world_size()

	for x in range(size):
		for y in range(size):
			while get_pos_x() < x:
				move(East)
			while get_pos_x() > x:
				move(West)
			while get_pos_y() < y:
				move(North)
			while get_pos_y() > y:
				move(South)

			if can_harvest():
				harvest()

			if get_ground_type() == Grounds.Soil:
				till()

			if get_entity_type() == None:
				plant(Entities.Grass)

			while not can_harvest() and get_entity_type() == Entities.Grass:
				if num_items(Items.Fertilizer) > 0:
					use_item(Items.Fertilizer)
				else:
					return

def farm_weird_substance():
	while True:
		farm_cycle()

if __name__ == "__main__":
	farm_weird_substance()
