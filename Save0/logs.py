def log(msg):
	quick_print(msg)

def log_pos():
	quick_print("pos: " + str(get_pos_x()) + "," + str(get_pos_y()))

def log_items():
	quick_print("hay:" + str(num_items(Items.Hay)))
	quick_print("wood:" + str(num_items(Items.Wood)))
	quick_print("carrot:" + str(num_items(Items.Carrot)))
	quick_print("pumpkin:" + str(num_items(Items.Pumpkin)))
	quick_print("power:" + str(num_items(Items.Power)))
