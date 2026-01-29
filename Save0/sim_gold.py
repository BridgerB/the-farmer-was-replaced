# =============================================================================
# GOLD MAZE SOLVER
# =============================================================================
# 
# Strategy: Distributed multi-drone maze solving
# - 32 drones spread across grid BEFORE maze spawns
# - Each drone uses backtracking algorithm to find treasure
# - First drone to reach treasure harvests it, others exit
#
# Performance: ~2.5s per maze, 84s to 1M gold
# =============================================================================

# -----------------------------------------------------------------------------
# MAZE SOLVING ALGORITHM
# -----------------------------------------------------------------------------
# 
# Uses depth-first search with backtracking:
# 1. Try to move toward treasure (priority directions)
# 2. If blocked, try other directions
# 3. If completely stuck, backtrack to previous position
# 4. Repeat until treasure found or no path exists
#
# Args:
#   tx: int - treasure X coordinate (from measure())
#   ty: int - treasure Y coordinate (from measure())
#
# Returns:
#   True if treasure found and harvested
#   False if not on a hedge or no path exists
# -----------------------------------------------------------------------------
def solve(tx, ty):
	# Track visited cells to avoid loops
	# Key: (x, y) tuple, Value: True
	visited = {}
	
	# Stack of moves made - used for backtracking
	# Contains direction constants (North, South, East, West)
	path = []
	
	# Cache position locally - avoid repeated API calls (1 tick each)
	x = get_pos_x()
	y = get_pos_y()
	
	while True:
		# --- CHECK: Are we on treasure? ---
		ent = get_entity_type()
		if ent == Entities.Treasure:
			harvest()
			return True
		
		# --- CHECK: Are we still in the maze? ---
		# Early return if we somehow left the maze
		if ent != Entities.Hedge:
			return False
		
		# --- MARK: Current cell as visited ---
		visited[(x, y)] = True
		
		# --- CALCULATE: Direction to treasure ---
		dx = tx - x  # Positive = treasure is East
		dy = ty - y  # Positive = treasure is North
		
		moved = False
		
		# --- TRY: Primary directions (toward treasure) ---
		# Prioritize the axis with greater distance
		if abs(dx) >= abs(dy):
			# Horizontal priority - try East/West first
			if dx > 0 and can_move(East) and (x+1, y) not in visited:
				move(East)
				path.append(East)
				x = x + 1
				moved = True
			elif dx < 0 and can_move(West) and (x-1, y) not in visited:
				move(West)
				path.append(West)
				x = x - 1
				moved = True
			elif dy > 0 and can_move(North) and (x, y+1) not in visited:
				move(North)
				path.append(North)
				y = y + 1
				moved = True
			elif dy < 0 and can_move(South) and (x, y-1) not in visited:
				move(South)
				path.append(South)
				y = y - 1
				moved = True
		else:
			# Vertical priority - try North/South first
			if dy > 0 and can_move(North) and (x, y+1) not in visited:
				move(North)
				path.append(North)
				y = y + 1
				moved = True
			elif dy < 0 and can_move(South) and (x, y-1) not in visited:
				move(South)
				path.append(South)
				y = y - 1
				moved = True
			elif dx > 0 and can_move(East) and (x+1, y) not in visited:
				move(East)
				path.append(East)
				x = x + 1
				moved = True
			elif dx < 0 and can_move(West) and (x-1, y) not in visited:
				move(West)
				path.append(West)
				x = x - 1
				moved = True
		
		# --- TRY: Any unvisited direction (when primary fails) ---
		if not moved:
			if can_move(North) and (x, y+1) not in visited:
				move(North)
				path.append(North)
				y = y + 1
				moved = True
			elif can_move(East) and (x+1, y) not in visited:
				move(East)
				path.append(East)
				x = x + 1
				moved = True
			elif can_move(South) and (x, y-1) not in visited:
				move(South)
				path.append(South)
				y = y - 1
				moved = True
			elif can_move(West) and (x-1, y) not in visited:
				move(West)
				path.append(West)
				x = x - 1
				moved = True
		
		# --- BACKTRACK: If completely stuck ---
		if not moved and len(path) > 0:
			# Pop last move and go opposite direction
			last = path.pop()
			if last == North:
				move(South)
				y = y - 1
			elif last == South:
				move(North)
				y = y + 1
			elif last == East:
				move(West)
				x = x - 1
			else:
				move(East)
				x = x + 1
		elif not moved:
			# No moves possible and nothing to backtrack - give up
			return False


# -----------------------------------------------------------------------------
# WORKER FACTORY
# -----------------------------------------------------------------------------
# 
# Creates a worker function that:
# 1. Moves toward target position using wrap-around (shortest path)
# 2. Checks for maze while moving - starts solving immediately when found
# 3. Only solves if actually inside maze (on Hedge)
#
# Args:
#   target_x: int - X coordinate to move toward
#   target_y: int - Y coordinate to move toward  
#   size: int - Grid size (for wrap-around calculation)
#
# Returns:
#   Function that can be passed to spawn_drone()
# -----------------------------------------------------------------------------
def make_worker(target_x, target_y, size):
	def worker():
		# --- CALCULATE: Shortest path using wrap-around ---
		# If target > half grid, go opposite direction (wraps around)
		# Example: target_x=28 on 32 grid -> go West 4 instead of East 28
		
		if target_x > size // 2:
			x_dir = West
			x_moves = size - target_x
		else:
			x_dir = East
			x_moves = target_x
		
		if target_y > size // 2:
			y_dir = South
			y_moves = size - target_y
		else:
			y_dir = North
			y_moves = target_y
		
		x_moved = 0
		y_moved = 0
		
		# --- MOVE: Toward target while checking for maze ---
		while x_moved < x_moves or y_moved < y_moves:
			# Check if maze appeared
			pos = measure()
			if pos != None:
				# Maze exists! Start solving if we're inside it
				if get_entity_type() == Entities.Hedge:
					solve(pos[0], pos[1])
				return
			
			# Keep moving toward target
			if x_moved < x_moves:
				move(x_dir)
				x_moved = x_moved + 1
			elif y_moved < y_moves:
				move(y_dir)
				y_moved = y_moved + 1
		
		# --- WAIT: For maze if we reached position before it spawned ---
		pos = measure()
		while pos == None:
			pos = measure()
		
		# --- SOLVE: If we're inside the maze ---
		if get_entity_type() == Entities.Hedge:
			solve(pos[0], pos[1])
	
	return worker


# -----------------------------------------------------------------------------
# POSITION DISTRIBUTION
# -----------------------------------------------------------------------------
# 
# Calculates evenly distributed positions across the grid.
# Uses a rectangular grid pattern that covers the full area.
#
# Args:
#   num_positions: int - How many positions to generate
#   size: int - Grid size (e.g., 32 for 32x32)
#
# Returns:
#   List of (x, y) tuples representing positions
#
# Example for 31 workers on 32x32:
#   Creates 6x6 grid (36 slots), uses first 31
#   Positions spread from ~(2,2) to ~(29,29)
# -----------------------------------------------------------------------------
def get_distributed_positions(num_positions, size):
	if num_positions <= 0:
		return []
	
	# --- CALCULATE: Grid dimensions ---
	# Find smallest square-ish grid that fits all positions
	cols = 1
	rows = 1
	while cols * rows < num_positions:
		if cols <= rows:
			cols = cols + 1
		else:
			rows = rows + 1
	
	# --- GENERATE: Positions with even spacing ---
	positions = []
	for row in range(rows):
		# Distribute remainder positions to first rows
		cols_in_row = num_positions // rows
		if row < (num_positions % rows):
			cols_in_row = cols_in_row + 1
		
		for col in range(cols_in_row):
			# Center each position within its cell
			# Formula: (size * (col*2 + 1)) // (cols_in_row * 2)
			px = (size * (col * 2 + 1)) // (cols_in_row * 2)
			py = (size * (row * 2 + 1)) // (rows * 2)
			positions.append((px, py))
	
	return positions


# -----------------------------------------------------------------------------
# SINGLE MAZE RUN
# -----------------------------------------------------------------------------
# 
# Executes one complete maze:
# 1. Go to origin (0,0)
# 2. Spawn workers at distributed positions
# 3. Brief wait for workers to start moving
# 4. Create maze
# 5. Main drone solves from origin
# 6. Wait for all workers to finish
#
# Gold yield: 32,768 per maze (32 * 32 * 32)
# -----------------------------------------------------------------------------
def run_maze():
	size = 32
	num_workers = max_drones() - 1  # Reserve 1 for main
	
	# --- SETUP: Calculate worker positions ---
	positions = get_distributed_positions(num_workers, size)
	
	# --- MOVE: Main to origin ---
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)
	
	# --- SPAWN: Workers (they start moving immediately) ---
	for p in positions:
		spawn_drone(make_worker(p[0], p[1], size))
	
	# --- WAIT: Brief pause for workers to start moving ---
	# 10 moves gives workers time to spread out
	for i in range(5):
		move(East)
	for i in range(5):
		move(West)
	
	# --- CREATE: Maze ---
	substance_cost = size * (2 ** max(0, num_unlocked(Unlocks.Mazes) - 1))
	if get_ground_type() == Grounds.Soil:
		till()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance_cost)
	
	# --- SOLVE: Main drone from origin ---
	pos = measure()
	while pos == None:
		pos = measure()
	solve(pos[0], pos[1])
	
	# --- CLEANUP: Wait for all workers to finish ---
	while num_drones() > 1:
		pass


# =============================================================================
# MAIN: Run benchmark to 1M gold
# =============================================================================

quick_print("=== 1M GOLD TEST ===")

clear()
set_world_size(32)

target = 1000000
start = get_time()
maze_count = 0

while num_items(Items.Gold) < target:
	run_maze()
	maze_count = maze_count + 1
	quick_print("Maze " + str(maze_count) + " at " + str(get_time() - start) + "s, gold=" + str(num_items(Items.Gold)))

total = get_time() - start
quick_print("---")
quick_print("DONE: " + str(num_items(Items.Gold)) + " gold")
quick_print("Mazes: " + str(maze_count))
quick_print("Total time: " + str(total) + "s")
