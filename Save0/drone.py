def get_zone_bounds():
	size = get_world_size()
	half = size // 2
	return [
		[0, half, 0, half],
		[half, size, 0, half],
		[0, half, half, size],
		[half, size, half, size]
	]

def wait_for_workers():
	while num_drones() > 1:
		pass

def spawn_zone_workers(worker_factory):
	zones = get_zone_bounds()
	for i in range(1, len(zones)):
		spawn_drone(worker_factory(zones[i][0], zones[i][1], zones[i][2], zones[i][3]))

def get_main_zone():
	zones = get_zone_bounds()
	return zones[0]

def run_parallel(worker_factory, main_fn):
	wait_for_workers()
	spawn_zone_workers(worker_factory)
	zone = get_main_zone()
	main_fn(zone[0], zone[1], zone[2], zone[3])
	wait_for_workers()
