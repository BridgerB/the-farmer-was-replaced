def move_snake(row):
    if row % 2 == 0:
        if get_pos_x() == get_world_size() - 1:
            move(South)
        else:
            move(East)
    else:
        if get_pos_x() == 0:
            move(South)
        else:
            move(West)

def do_tile():
    # Always harvest anything ready
    if can_harvest():
        harvest()
    # Plant bush if empty or try to clear dead stuff
    if get_entity_type() == None:
        plant(Entities.Bush)
    elif not can_harvest():
        # Try planting over dead pumpkins etc
        plant(Entities.Bush)

def farm_cycle():
    size = get_world_size()
    for row in range(size):
        for col in range(size):
            do_tile()
            move_snake(row)

def farm_wood():
    while True:
        farm_cycle()

if __name__ == "__main__":
    farm_wood()
