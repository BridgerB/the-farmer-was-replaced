import movement

def go_to(x, y):
    while get_pos_x() < x:
        move(East)
    while get_pos_x() > x:
        move(West)
    while get_pos_y() < y:
        move(North)
    while get_pos_y() > y:
        move(South)

def farm_cycle():
    size = get_world_size()
    total = size * size

    # Phase 1: Plant all pumpkins, track all positions
    movement.go_to_start()
    not_ready = []
    for i in range(total):
        if get_ground_type() != Grounds.Soil:
            till()
        if get_water() < 0.8 and num_items(Items.Water) > 0:
            use_item(Items.Water)
        if can_harvest() and get_entity_type() != Entities.Pumpkin:
            harvest()
        if get_entity_type() == None:
            if num_items(Items.Carrot) > 0:
                plant(Entities.Pumpkin)

        not_ready.append([get_pos_x(), get_pos_y()])
        movement.move_next()

    # Phase 2: Only visit unconfirmed positions
    while len(not_ready) > 0:
        still_not_ready = []

        for pos in not_ready:
            go_to(pos[0], pos[1])

            if get_water() < 0.8 and num_items(Items.Water) > 0:
                use_item(Items.Water)

            if can_harvest():
                pass
            else:
                if num_items(Items.Carrot) > 0:
                    plant(Entities.Pumpkin)
                still_not_ready.append(pos)

        not_ready = still_not_ready

    # Phase 3: Harvest the giant
    movement.go_to_start()
    harvest()

def farm_pumpkin():
    while True:
        farm_cycle()

if __name__ == "__main__":
    farm_pumpkin()
