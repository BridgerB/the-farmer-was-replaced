def worker():
	while num_items(Items.Hay) < 10000000:
		harvest()
		move(North)

start = get_time()
size = get_world_size()
spawn_drone(worker)
for c in range(size - 2):
	move(East)
	spawn_drone(worker)
move(East)
while num_items(Items.Hay) < 10000000:
	harvest()
	move(North)
quick_print("Hay: " + str(num_items(Items.Hay)))
quick_print("Time to 10M: " + str(get_time() - start) + "s")
