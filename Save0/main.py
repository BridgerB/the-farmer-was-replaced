import logs
import resources
import hay
import wood
import carrot
import pumpkin
import sunflower
import substance
import maze
import cactus
import dinosaur
import hamiltonian

MODE = "goals"
CARROT_BUFFER = 1000
goals_rotation = 0

def try_buy_expand():
	cost = get_cost(Unlocks.Expand)
	if cost == None:
		return False
	can_afford = True
	for item in cost:
		if num_items(item) < cost[item]:
			can_afford = False
	if can_afford:
		logs.log("EXPAND AFFORDABLE - purchasing")
		unlock(Unlocks.Expand)
		logs.log("bought expand, new world_size=" + str(get_world_size()))
		return True
	return False

def goals_cycle():
	global goals_rotation
	if try_buy_expand():
		return
	if num_items(Items.Power) < 500:
		logs.log("goals: power low (have " + str(num_items(Items.Power)) + "), sunflower")
		sunflower_mode()
		return
	if num_unlocked(Unlocks.Expand) < 30 and get_world_size() < 88:
		pumpkin_for_expand = True
	else:
		pumpkin_for_expand = False

	goals_rotation = goals_rotation + 1
	slot = goals_rotation % 4

	if num_items(Items.Gold) < 1000000 and slot == 0:
		logs.log("goals: gold (have " + str(num_items(Items.Gold)) + ")")
		maze.cycle()
	elif pumpkin_for_expand and slot != 3:
		logs.log("goals: pumpkin-for-expand (have " + str(num_items(Items.Pumpkin)) + ")")
		pumpkin_mode()
	else:
		logs.log("goals: bones (have " + str(num_items(Items.Bone)) + ")")
		dinosaur.cycle()

def run_crop(name):
	if name == "hay":
		hay.cycle()
	elif name == "wood":
		wood.cycle()
	elif name == "carrot":
		carrot.cycle()
	elif name == "pumpkin":
		pumpkin.cycle()
	elif name == "sunflower" or name == "power":
		sunflower.cycle()
	elif name == "substance":
		substance.cycle()
	elif name == "gold":
		maze.cycle()
	elif name == "cactus":
		cactus.cycle()
	elif name == "bones":
		dinosaur.cycle()
	elif name == "hamiltonian":
		hamiltonian.cycle()

def auto_cycle():
	crop = resources.get_next_crop()
	logs.log("auto: " + crop)
	run_crop(crop)

def pumpkin_mode():
	if num_items(Items.Hay) < 10:
		return hay.cycle()
	if num_items(Items.Wood) < 10:
		return wood.cycle()
	if num_items(Items.Carrot) < CARROT_BUFFER:
		carrot.cycle()
		return
	pumpkin.cycle()
	if num_items(Items.Carrot) < 100:
		carrot.cycle()

def sunflower_mode():
	sunflower.cycle()
	if num_items(Items.Carrot) >= 100:
		return
	if not resources.has_hay():
		return hay.cycle()
	if not resources.has_wood():
		return wood.cycle()
	carrot.cycle()

def main():
	logs.log("starting main")
	logs.log_items()
	while True:
		if MODE == "goals":
			goals_cycle()
		elif MODE == "auto":
			auto_cycle()
		elif MODE == "hay":
			hay.cycle()
		elif MODE == "wood":
			wood.cycle()
		elif MODE == "carrot":
			carrot.cycle()
		elif MODE == "pumpkin":
			pumpkin_mode()
		elif MODE == "sunflower":
			sunflower_mode()
		elif MODE == "substance":
			substance.cycle()
		elif MODE == "gold":
			maze.cycle()
		elif MODE == "bones":
			dinosaur.cycle()
		elif MODE == "hamiltonian":
			hamiltonian.cycle()
			break

if __name__ == "__main__":
	main()
