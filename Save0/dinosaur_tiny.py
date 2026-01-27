import logs
import nav

def cycle():
	set_world_size(5)

	nav.go_to(0, 0)
	if get_entity_type() != None:
		harvest()

	change_hat(Hats.Dinosaur_Hat)

	while num_items(Items.Cactus) >= 100:
		for i in range(4):
			move(East)
		move(North)
		for i in range(3):
			move(West)
		move(North)
		for i in range(3):
			move(East)
		move(North)
		for i in range(3):
			move(West)
		move(North)
		for i in range(3):
			move(East)
		move(East)
		for i in range(4):
			move(South)

	change_hat(Hats.Straw_Hat)
	logs.log("Total bones: " + str(num_items(Items.Bone)))
