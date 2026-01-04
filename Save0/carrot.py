import movement

def can_afford(entity):
    cost = get_cost(entity)
    for item in cost:
        if num_items(item) < cost[item]:
            return False
    return True

def process_tile():
    # Harvest if ready
    if can_harvest():
        harvest()

    # Ensure soil
    if get_ground_type() != Grounds.Soil:
        till()

    # Plant carrot if we can afford it
    if can_afford(Entities.Carrot):
        plant(Entities.Carrot)

def farm_cycle():
    # Early exit if we can't afford carrots
    if not can_afford(Entities.Carrot):
        return

    movement.traverse_all(process_tile)

def farm_carrot():
    while True:
        farm_cycle()

if __name__ == "__main__":
    farm_carrot()
