import hay
import wood
import tree
import carrot
import pumpkin
import sunflower
import maze
import weird_substance
import movement

# Override: "auto", "hay", "wood", "carrot", "pumpkin", "sunflower", "maze"
FARM_MODE = "maze"

def random_move():
	# Try to unstick by moving in any available direction
	for d in [North, East, South, West]:
		if move(d):
			return True
	return False

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

def check_dependencies(mode):
	# Only switch modes if completely out of required resource
	if mode == "pumpkin" or mode == "sunflower":
		if num_items(Items.Carrot) == 0:
			# Need carrots - but first check carrot dependencies
			if num_items(Items.Hay) == 0:
				return "hay"
			if num_items(Items.Wood) == 0:
				return "wood"
			return "carrot"

	if mode == "carrot":
		if num_items(Items.Hay) == 0:
			return "hay"
		if num_items(Items.Wood) == 0:
			return "wood"

	return mode  # Dependencies met

def can_afford(entity):
	cost = get_cost(entity)
	for item in cost:
		if num_items(item) < cost[item]:
			return False
	return True

def get_missing_resource(entity):
	# Returns which resource we're short on, or None if we can afford
	cost = get_cost(entity)
	for item in cost:
		if num_items(item) < cost[item]:
			return item
	return None

def main():
	while True:
		if FARM_MODE == "pumpkin":
			if can_afford(Entities.Pumpkin):
				pumpkin.farm_cycle()
			elif can_afford(Entities.Carrot):
				carrot.farm_cycle()
			else:
				# Need resources for carrots - check what's missing
				missing = get_missing_resource(Entities.Carrot)
				if missing == Items.Hay:
					hay.farm_cycle()
				else:
					tree.farm_cycle()
		elif FARM_MODE == "sunflower":
			if can_afford(Entities.Sunflower):
				sunflower.farm_cycle()
			elif can_afford(Entities.Carrot):
				carrot.farm_cycle()
			else:
				missing = get_missing_resource(Entities.Carrot)
				if missing == Items.Hay:
					hay.farm_cycle()
				else:
					tree.farm_cycle()
		elif FARM_MODE == "maze":
			# Calculate weird substance needed for maze
			size = get_world_size()
			substance_needed = size * (2 ** max(0, num_unlocked(Unlocks.Mazes) - 1))
			if num_items(Items.Weird_Substance) >= substance_needed:
				maze.farm_cycle()
			else:
				# Need more weird substance - farm fertilized grass
				weird_substance.farm_cycle()
		elif FARM_MODE == "auto":
			resource = get_what_to_farm()
			farm_one_cycle(resource)
		else:
			resource = check_dependencies(FARM_MODE)
			farm_one_cycle(resource)

if __name__ == "__main__":
	main()
