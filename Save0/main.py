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

MODE = "bones"
CARROT_BUFFER = 1000

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
		if MODE == "auto":
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
