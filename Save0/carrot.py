import movement

def process_tile():
    # Harvest if ready
    if can_harvest():
        harvest()

    # Ensure soil
    if get_ground_type() != Grounds.Soil:
        till()

    # Plant if we have resources and tile is empty or dead
    if num_items(Items.Hay) > 0 and num_items(Items.Wood) > 0:
        if not can_harvest():
            plant(Entities.Carrot)

def farm_cycle():
    movement.traverse_all(process_tile)

def farm_carrot():
    while True:
        farm_cycle()

if __name__ == "__main__":
    farm_carrot()
