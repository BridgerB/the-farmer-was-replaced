def move_to_next():
    move(East)
    if get_pos_x() == 0:
        move(South)

def do_tile():
    # Always harvest anything ready first
    if can_harvest():
        harvest()
    # Ensure soil
    if get_ground_type() != Grounds.Soil:
        till()
    # Water for faster growth
    if get_water() < 0.8 and num_items(Items.Water) > 0:
        use_item(Items.Water)
    # Plant if empty or clear dead stuff
    if num_items(Items.Carrot) > 0:
        if get_entity_type() == None or not can_harvest():
            plant(Entities.Pumpkin)

def count_ready():
    count = 0
    size = get_world_size()
    for i in range(size * size):
        if can_harvest():
            count = count + 1
        move_to_next()
    return count

def harvest_all():
    size = get_world_size()
    for i in range(size * size):
        if can_harvest():
            harvest()
        move_to_next()

def farm_cycle():
    size = get_world_size()
    for i in range(size * size):
        do_tile()
        move_to_next()
    ready = count_ready()
    if ready == size * size:
        harvest_all()

def farm_pumpkin():
    while True:
        farm_cycle()

if __name__ == "__main__":
    farm_pumpkin()
