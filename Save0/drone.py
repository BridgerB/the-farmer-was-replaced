def get_zone_bounds():
	size = get_world_size()
	total = max_drones()
	cols = max(1, size // total)
	zones = []
	for i in range(total):
		start = i * cols
		if i == total - 1:
			end = size
		else:
			end = start + cols
		zones.append([start, end])
	return zones

def wait_for_workers():
	while num_drones() > 1:
		pass

def spawn_zone_workers(worker_factory):
	zones = get_zone_bounds()
	for i in range(1, len(zones)):
		spawn_drone(worker_factory(zones[i][0], zones[i][1]))

def get_main_zone():
	zones = get_zone_bounds()
	return zones[0]

def run_parallel(worker_factory, main_fn):
	wait_for_workers()
	spawn_zone_workers(worker_factory)
	zone = get_main_zone()
	main_fn(zone[0], zone[1])
	wait_for_workers()
