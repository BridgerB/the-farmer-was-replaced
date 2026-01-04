def move_clockwise():
    x = get_pos_x()
    y = get_pos_y()
    size = get_world_size()
    if y == size - 1 and x < size - 1:
        move(East)
    elif x == size - 1 and y > 0:
        move(South)
    elif y == 0 and x > 0:
        move(West)
    elif x == 0 and y < size - 1:
        move(North)
    else:
        move(East)

def do_tile():
    # Always harvest anything ready
    if can_harvest():
        harvest()
    # Ensure soil for carrots
    if get_ground_type() != Grounds.Soil:
        till()
    # Plant if empty or clear dead stuff
    if get_entity_type() == None or not can_harvest():
        plant(Entities.Carrot)

def farm_cycle():
    size = get_world_size()
    for i in range(size * size):
        do_tile()
        move_clockwise()

def farm_carrot():
    while True:
        farm_cycle()

if __name__ == "__main__":
    farm_carrot()
