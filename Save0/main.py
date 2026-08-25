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
CARROT_BUFFER = 5000
goals_rotation = 0
sunflower_stall_count = 0

def note_sunflower_result(gained):
	global sunflower_stall_count
	if gained:
		sunflower_stall_count = 0
	else:
		sunflower_stall_count = sunflower_stall_count + 1
	return sunflower_stall_count

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

leaderboard_cost_logged = False

def try_buy_leaderboard():
	global leaderboard_cost_logged
	if num_unlocked(Unlocks.Leaderboard) > 0:
		return False
	cost = get_cost(Unlocks.Leaderboard)
	if cost == None:
		return False
	if not leaderboard_cost_logged:
		leaderboard_cost_logged = True
		for item in cost:
			logs.log("leaderboard cost: " + str(item) + " needs " + str(cost[item]) + ", have " + str(num_items(item)))
	can_afford = True
	for item in cost:
		if num_items(item) < cost[item]:
			can_afford = False
	if can_afford:
		logs.log("LEADERBOARD AFFORDABLE - purchasing")
		unlock(Unlocks.Leaderboard)
		logs.log("bought Unlocks.Leaderboard")
		return True
	return False

def goals_cycle():
	global goals_rotation
	if try_buy_expand():
		return
	if try_buy_leaderboard():
		return
	if num_items(Items.Power) < 500:
		power_before_sf = num_items(Items.Power)
		logs.log("goals: power low (have " + str(power_before_sf) + "), sunflower")
		sunflower_mode()
		stall_count = note_sunflower_result(num_items(Items.Power) > power_before_sf)
		if stall_count < 5:
			return
		logs.log("goals: sunflower stalled " + str(stall_count) + "x (field likely saturated with growing pumpkins), proceeding despite low power")
	if num_unlocked(Unlocks.Leaderboard) == 0 and num_items(Items.Gold) < 1000000:
		logs.log("goals: gold low (have " + str(num_items(Items.Gold)) + "), maze")
		maze.cycle()
		return

	if num_unlocked(Unlocks.Expand) < 30 and get_world_size() < 88:
		pumpkin_for_expand = True
	else:
		pumpkin_for_expand = False

	goals_rotation = goals_rotation + 1
	slot = goals_rotation % 4

	if pumpkin_for_expand and slot != 3:
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
