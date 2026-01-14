import nav
import drone
import logs

def plant_cell(x, y):
	if get_ground_type() != Grounds.Soil:
		till()
	entity = get_entity_type()
	if entity != Entities.Cactus:
		if entity != None and can_harvest():
			harvest()
		if get_entity_type() == None:
			plant(Entities.Cactus)

def plant_zone(x_start, x_end, y_start, y_end):
	nav.traverse_zone(x_start, x_end, y_start, y_end, plant_cell)

def make_plant_worker(x_start, x_end, y_start, y_end):
	def worker():
		plant_zone(x_start, x_end, y_start, y_end)
	return worker

def wait_cell(x, y):
	if get_entity_type() == Entities.Cactus:
		while not can_harvest():
			pass

def wait_zone(x_start, x_end, y_start, y_end):
	nav.traverse_zone(x_start, x_end, y_start, y_end, wait_cell)

def make_wait_worker(x_start, x_end, y_start, y_end):
	def worker():
		wait_zone(x_start, x_end, y_start, y_end)
	return worker

def sort_row(y):
	size = get_world_size()
	swapped = True
	while swapped:
		swapped = False
		for x in range(size - 1):
			nav.go_to(x, y)
			if get_entity_type() != Entities.Cactus:
				continue
			left_size = measure()
			right_size = measure(East)
			if right_size != None and left_size > right_size:
				swap(East)
				swapped = True

def sort_col(x):
	size = get_world_size()
	swapped = True
	while swapped:
		swapped = False
		for y in range(size - 1):
			nav.go_to(x, y)
			if get_entity_type() != Entities.Cactus:
				continue
			bottom_size = measure()
			top_size = measure(North)
			if top_size != None and bottom_size > top_size:
				swap(North)
				swapped = True

def get_balanced_ranges(total, num_workers):
	ranges = []
	base = total // num_workers
	remainder = total % num_workers
	start = 0
	for i in range(num_workers):
		count = base
		if i < remainder:
			count = count + 1
		if count > 0 and start < total:
			ranges.append([start, start + count])
			start = start + count
	return ranges

def make_row_sort_worker(y_start, y_end):
	def worker():
		for row in range(y_start, y_end):
			sort_row(row)
	return worker

def make_col_sort_worker(x_start, x_end):
	def worker():
		for col in range(x_start, x_end):
			sort_col(col)
	return worker

def sort_rows_parallel():
	size = get_world_size()
	num_workers = max_drones()
	if num_workers > size:
		num_workers = size
	ranges = get_balanced_ranges(size, num_workers)
	drone.wait_for_workers()
	for i in range(1, len(ranges)):
		spawn_drone(make_row_sort_worker(ranges[i][0], ranges[i][1]))
	if len(ranges) > 0:
		for row in range(ranges[0][0], ranges[0][1]):
			sort_row(row)
	drone.wait_for_workers()

def sort_cols_parallel():
	size = get_world_size()
	num_workers = max_drones()
	if num_workers > size:
		num_workers = size
	ranges = get_balanced_ranges(size, num_workers)
	drone.wait_for_workers()
	for i in range(1, len(ranges)):
		spawn_drone(make_col_sort_worker(ranges[i][0], ranges[i][1]))
	if len(ranges) > 0:
		for col in range(ranges[0][0], ranges[0][1]):
			sort_col(col)
	drone.wait_for_workers()

def cycle():
	logs.log("cactus cycle")
	drone.run_parallel(make_plant_worker, plant_zone)
	drone.run_parallel(make_wait_worker, wait_zone)
	sort_rows_parallel()
	sort_cols_parallel()
	nav.go_to(0, 0)
	harvest()
