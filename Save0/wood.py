import movement

def process_tile():
    # Harvest if ready
    if can_harvest():
        harvest()

    # Plant bush if empty or dead
    if not can_harvest():
        plant(Entities.Bush)

def farm_cycle():
    movement.traverse_all(process_tile)

def farm_wood():
    while True:
        farm_cycle()

if __name__ == "__main__":
    farm_wood()
