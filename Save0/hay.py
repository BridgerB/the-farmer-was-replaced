import movement

def process_tile():
    # Harvest if ready
    if can_harvest():
        harvest()

    # Convert soil back to grass for hay
    if get_ground_type() == Grounds.Soil:
        till()

def farm_cycle():
    movement.traverse_all(process_tile)

def farm_hay():
    while True:
        farm_cycle()

if __name__ == "__main__":
    farm_hay()
