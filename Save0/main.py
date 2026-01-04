import hay
import wood
import tree
import carrot
import pumpkin

# Cycles per "60 seconds" - adjust based on game speed
CYCLES_PER_CHECK = 10

def get_lowest_resource():
    h = num_items(Items.Hay)
    w = num_items(Items.Wood)
    c = num_items(Items.Carrot)
    p = num_items(Items.Pumpkin)

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

    return lowest

def farm_for(resource, cycles):
    for i in range(cycles):
        if resource == "hay":
            hay.farm_cycle()
        elif resource == "wood":
            wood.farm_cycle()
        elif resource == "carrot":
            carrot.farm_cycle()
        elif resource == "pumpkin":
            pumpkin.farm_cycle()

def main():
    while True:
        resource = get_lowest_resource()
        farm_for(resource, CYCLES_PER_CHECK)

if __name__ == "__main__":
    main()
