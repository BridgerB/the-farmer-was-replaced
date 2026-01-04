import hay
import wood
import tree
import carrot
import pumpkin
import sunflower
import movement

# Override: "auto", "hay", "wood", "carrot", "pumpkin", "sunflower"
FARM_MODE = "pumpkin"

def get_what_to_farm():
    h = num_items(Items.Hay)
    w = num_items(Items.Wood)
    c = num_items(Items.Carrot)
    p = num_items(Items.Pumpkin)
    pw = num_items(Items.Power)

    # Check dependencies first:
    # - Carrots need hay + wood
    # - Pumpkins need carrots
    # - Sunflowers need carrots (like pumpkins)

    # If we can't plant carrots, farm hay or wood first
    if h == 0:
        return "hay"
    if w == 0:
        return "wood"

    # If we can't plant pumpkins/sunflowers, farm carrots first
    if c == 0:
        return "carrot"

    # Now find actual lowest
    lowest = "hay"
    lowest_val = h

    if w < lowest_val:
        lowest = "wood"
        lowest_val = w
    if c < lowest_val:
        lowest = "carrot"
        lowest_val = c
    if p < lowest_val:
        lowest = "pumpkin"
        lowest_val = p
    if pw < lowest_val:
        lowest = "sunflower"
        lowest_val = pw

    return lowest

def farm_one_cycle(resource):
    if resource == "hay":
        hay.farm_cycle()
    elif resource == "wood":
        tree.farm_cycle()
    elif resource == "carrot":
        carrot.farm_cycle()
    elif resource == "pumpkin":
        pumpkin.farm_cycle()
    elif resource == "sunflower":
        sunflower.farm_cycle()

def main():
    while True:
        if FARM_MODE == "auto":
            resource = get_what_to_farm()
        else:
            resource = FARM_MODE
        farm_one_cycle(resource)

if __name__ == "__main__":
    main()
