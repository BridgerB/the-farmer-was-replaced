# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Automation scripts for "The Farmer Was Replaced" - a farming game where you write Python-like code to control drones that farm crops on a grid-based field.

## Language Constraints (CRITICAL)

The game uses a Python-like language with these limitations:
- **No ternary expressions**: `x if cond else y` causes syntax error - use if/else blocks
- **No import aliasing**: `import x as y` and `from x import y as z` fail
- **No subdirectory imports**: All files must be in root, use `import module` then `module.function()`
- **Workers cannot return data**: `spawn_drone()` workers can't send data back to main
- **Tuples work**: `(x, y)` can be used, including as dict keys `{(1,2): value}`
- **No f-strings**: Use `"text" + str(value)` for string concatenation

## Game Fundamentals

### The Grid
- Field is a square grid of size `get_world_size()` (expands as you unlock)
- Coordinates: (0,0) is bottom-left (South-West corner)
- X increases going East, Y increases going North
- Movement wraps around edges (move East from right edge → appear on left)

### Ticks (Performance)
- Actions (move, plant, harvest, till) cost **200 ticks**
- Checks (get_pos, get_entity_type, measure, can_harvest) cost **1 tick**
- `quick_print()` costs **0 ticks** (use for logging)
- `print()` costs **1 second real time** (displays smoke above drone)

### Ground Types
- `Grounds.Grassland` - Default ground, grass grows automatically
- `Grounds.Soil` - Created by `till()`, required for carrots/pumpkins/sunflowers/cactus
- Calling `till()` toggles between Grassland and Soil

## All Entities (Crops/Objects)

### Entities.Grass
- Grows on: Grassland or Soil
- Growth time: ~0.5 seconds
- Yields: `Items.Hay`
- Plant with: `plant(Entities.Grass)`

### Entities.Bush
- Grows on: Grassland or Soil
- Growth time: ~4 seconds
- Yields: `Items.Wood`
- Also used to spawn mazes with Weird_Substance

### Entities.Tree
- Grows on: Grassland or Soil
- Growth time: ~7 seconds (SLOWER if adjacent to other trees)
- Yields: `Items.Wood` (more than bushes)
- Best practice: Checkerboard pattern with bushes to avoid slowdown

### Entities.Carrot
- Grows on: Soil only
- Growth time: ~6 seconds
- Yields: `Items.Carrot`
- Cost: `Items.Carrot` to plant (need carrots to make carrots)

### Entities.Pumpkin
- Grows on: Soil only
- Growth time: ~2 seconds
- Yields: `Items.Pumpkin`
- Cost: `Items.Carrot` to plant
- **Special mechanics:**
  - ~20% of pumpkins die → become `Entities.Dead_Pumpkin`
  - Adjacent fully-grown pumpkins merge into "mega pumpkin"
  - Yield = (number of connected pumpkins)³
  - Water level affects growth: use `use_item(Items.Water)` when `get_water() < 0.8`
  - **Must wait for ALL to be ready before harvesting any**

### Entities.Sunflower
- Grows on: Soil only
- Growth time: 5.6-8.4 seconds
- Yields: `Items.Power`
- Cost: `Items.Carrot` to plant
- **Special mechanics:**
  - Each sunflower has 7-15 petals (random)
  - `measure()` returns petal count (works BEFORE fully grown)
  - **8x power bonus** if:
    1. At least 10 sunflowers on field
    2. You harvest the one(s) with MOST petals first
  - If you harvest a lower-petal sunflower while higher exists → lose bonus on next harvest too
  - Multiple sunflowers can tie for max petals

### Entities.Cactus
- Grows on: Soil only
- Growth time: ~1 second
- Yields: `Items.Cactus`
- **Special mechanics:**
  - Each cactus has size 0-9
  - `measure()` returns size
  - Harvesting triggers chain: adjacent cacti in sorted order also harvest
  - Yield = (number of chained cacti)²
  - Requires sorting algorithm to maximize

### Entities.Hedge
- Part of maze structure
- Cannot be harvested, blocks movement
- Use `can_move(direction)` to check for walls

### Entities.Treasure
- Found in center of mazes
- `harvest()` to collect `Items.Gold`
- Gold amount = maze side length

### Entities.Dinosaur
- Special mini-game with Dinosaur_Hat
- Tail follows drone, `measure()` returns type number

### Entities.Dead_Pumpkin
- Failed pumpkin (~20% chance)
- `can_harvest()` returns False
- Disappears when you plant something new

## All Items

### Items.Hay
- From: Harvesting grass
- Used for: Unlocks, purchases

### Items.Wood
- From: Harvesting bushes and trees
- Used for: Unlocks, purchases

### Items.Carrot
- From: Harvesting carrots
- Used for: Planting carrots, pumpkins, sunflowers

### Items.Pumpkin
- From: Harvesting pumpkins
- Used for: Unlocks, purchases

### Items.Power
- From: Harvesting sunflowers
- Effect: Drone moves 2x faster automatically while you have power
- Consumed automatically during movement

### Items.Water
- Use with: `use_item(Items.Water)`
- Effect: Waters ground under drone
- Check level: `get_water()` returns 0.0-1.0

### Items.Fertilizer
- Use with: `use_item(Items.Fertilizer)`
- Effect: Reduces plant growth time by 2 seconds instantly
- Used for: Farming Weird_Substance efficiently

### Items.Weird_Substance
- From: Harvesting fertilized grass (complex process)
- Use with: `use_item(Items.Weird_Substance)` on a bush → creates maze
- Amount needed for maze: `size * (2 ** max(0, num_unlocked(Unlocks.Mazes) - 1))`

### Items.Gold
- From: Maze treasures
- Used for: Unlocks, leaderboards

### Items.Cactus
- From: Harvesting sorted cacti chains
- Used for: Unlocks, leaderboards

### Items.Bone
- From: Dinosaur mini-game
- Used for: Unlocks, leaderboards

## Core API Functions

### Movement
```python
move(direction)        # Move one tile (North/East/South/West), returns bool
can_move(direction)    # Check if can move (for mazes), returns bool
get_pos_x()           # Current X coordinate
get_pos_y()           # Current Y coordinate
get_world_size()      # Grid side length
```

### Farming
```python
plant(entity)         # Plant entity, costs resources, returns bool
harvest()             # Harvest/destroy entity under drone, returns bool
can_harvest()         # Check if entity is fully grown, returns bool
till()                # Toggle ground between Grassland/Soil
```

### Sensing
```python
get_entity_type()     # Returns Entity or None
get_ground_type()     # Returns Grounds.Grassland or Grounds.Soil
get_water()           # Returns 0.0-1.0 water level
measure()             # Entity-specific: petals/size/treasure_pos
measure(direction)    # Measure adjacent entity
get_companion()       # For polyculture bonus, returns (type, (x,y)) or None
```

### Items
```python
num_items(item)           # How many of item you have
use_item(item)            # Use item (Water/Fertilizer/Weird_Substance)
use_item(item, count)     # Use multiple
```

### Multi-Drone
```python
spawn_drone(function)     # Spawn worker running function, returns handle or None
max_drones()              # Maximum allowed drones
num_drones()              # Current drone count
wait_for(handle)          # Wait for specific drone, get return value
has_finished(handle)      # Check if drone is done
```

### Utility
```python
quick_print(msg)          # Log to output.txt (0 ticks)
print(msg)                # Display in smoke (1 second delay)
get_time()                # Seconds since game start
get_tick_count()          # Total ticks executed
random()                  # Random float [0, 1)
clear()                   # Reset entire farm
```

### Unlocks
```python
unlock(unlock)            # Purchase unlock
num_unlocked(thing)       # Check unlock level (0 = locked)
get_cost(thing)           # Get cost dict {Item: amount}
```

### Debug
```python
set_execution_speed(n)    # Limit speed (1 = base, 10 = fast, 0.5 = slow)
set_world_size(n)         # Shrink grid for testing (min 3)
```

## Architecture

### File Structure

**Utils (shared helpers):**
- `nav.py` - Navigation utilities
- `drone.py` - Multi-drone coordination
- `resources.py` - Resource tracking and auto-crop selection
- `logs.py` - Logging wrapper

**Crops (each exports `cycle()`):**
- `hay.py` - Grass farming
- `wood.py` - Tree/bush farming
- `carrot.py` - Carrot farming
- `pumpkin.py` - Pumpkin mega-farm
- `sunflower.py` - Sunflower power farming
- `substance.py` - Weird substance production
- `maze.py` - Maze solving for gold

**Entry point:**
- `main.py` - Mode-based controller

### nav.py - Navigation

```python
go_to(x, y)
# Moves drone to target coordinates using cardinal directions

s_shape_range(start_col, end_col, size)
# Returns list of [x, y] positions in S-pattern for efficient traversal
# Even columns: bottom to top
# Odd columns: top to bottom
# Minimizes movement between columns

traverse_zone(start_col, end_col, cell_fn)
# Traverses zone calling cell_fn(x, y) at each position
```

### drone.py - Multi-Drone Coordination

```python
get_zone_bounds()
# Splits field into vertical zones, one per drone
# Returns list of [start_col, end_col] pairs
# Last zone gets remainder columns

wait_for_workers()
# Blocks until only main drone remains (num_drones() == 1)

spawn_zone_workers(worker_factory)
# Spawns workers for zones 1+ (main handles zone 0)
# worker_factory(start_col, end_col) must return a function

get_main_zone()
# Returns [start_col, end_col] for zone 0 (main drone's zone)

run_parallel(worker_factory, main_fn)
# Complete parallel operation:
# 1. Wait for any existing workers
# 2. Spawn zone workers
# 3. Main executes main_fn on zone 0
# 4. Wait for all workers to finish
```

### resources.py - Resource Management

```python
has_hay() / has_wood() / has_carrot()
# Quick checks for non-zero amounts

get_lowest_resource()
# Returns name of resource with lowest count
# Checks: hay, wood, carrot, pumpkin, power, gold

get_next_crop()
# Auto-mode logic:
# 1. If no hay → "hay"
# 2. If no wood → "wood"
# 3. If no carrot → "carrot"
# 4. Otherwise → lowest resource
```

### main.py - Entry Point

```python
MODE = "auto"  # or "hay", "wood", "carrot", "pumpkin", "sunflower", "substance", "gold"

run_crop(name)
# Dispatches to appropriate crop cycle

auto_cycle()
# Uses get_next_crop() to pick and farm

pumpkin_mode()
# Maintains minimum hay/wood/carrot before pumpkins

sunflower_mode()
# Farms sunflowers, maintains carrot supply

main()
# Infinite loop running selected mode
```

## Crop Implementation Patterns

### Simple Crop Pattern (hay, wood, carrot)

```python
def farm_cell(x, y):
    # Prepare ground if needed
    if get_ground_type() != Grounds.Soil:
        till()
    # Harvest if ready
    if can_harvest():
        harvest()
    # Plant if empty
    if get_entity_type() == None:
        plant(Entities.Something)

def farm_zone(start_col, end_col):
    nav.traverse_zone(start_col, end_col, farm_cell)

def make_worker(start_col, end_col):
    def worker():
        farm_zone(start_col, end_col)
    return worker

def cycle():
    drone.run_parallel(make_worker, farm_zone)
```

### Pumpkin Pattern (synchronized harvest)

1. Plant all pumpkins with water
2. Track positions that aren't ready
3. Loop until all ready (checking not_ready list)
4. Single harvest() triggers mega-pumpkin collection
5. All drones must sync before harvest

### Sunflower Pattern (ordered harvest)

1. Plant in parallel across zones
2. Wait for all to be harvestable
3. For each petal count 15 → 7:
   - All drones harvest that petal count from their zones
   - Wait for sync before next petal count
4. Ensures highest petals harvested first for 8x bonus

### Maze Pattern (parallel pathfinding)

1. Check substance requirements
2. Plant bush at (0,0), use Weird_Substance
3. `measure()` returns treasure position
4. Spawn multiple drones with different direction priorities
5. Each uses backtracking: visited list + path stack
6. First to reach treasure harvests it

## Code Style Guidelines

- Pure functional code, no comments
- Early returns where possible
- Use closures for worker factories
- Use `nav.s_shape_range()` for efficient traversal
- Always `drone.wait_for_workers()` before spawning new workers
- Check resource requirements before expensive operations

## Common Patterns

### Closure-based Worker Factory
```python
def make_worker(start_col, end_col):
    def worker():
        # Worker code here, can access start_col, end_col
        pass
    return worker
```

### Zone-based Parallel Farming
```python
def cycle():
    drone.wait_for_workers()
    drone.spawn_zone_workers(make_worker)
    zone = drone.get_main_zone()
    do_work(zone[0], zone[1])
    drone.wait_for_workers()
```

### Petal Map for Sunflowers
```python
petal_map = {}
for i in range(7, 16):
    petal_map[i] = []
# During planting:
petals = measure()
petal_map[petals].append((x, y))
```

### Waiting for Growth
```python
# Wait on a known position
nav.go_to(x, y)
while not can_harvest():
    pass
```

### Safe Planting
```python
if get_entity_type() == None and num_items(Items.Carrot) > 0:
    plant(Entities.Sunflower)
```

## Debugging Tips

- Use `quick_print()` liberally - it's free (0 ticks)
- `set_execution_speed(1)` to slow down and watch
- `set_world_size(3)` to test on tiny grid
- Check `num_drones()` if workers seem stuck
- Verify `can_harvest()` before assuming entity is ready
- `get_entity_type() == None` check before planting

## Performance Optimization

- Minimize movement - use S-shape patterns
- Parallel operations via zone splitting
- `quick_print()` over `print()` (0 vs 1000ms)
- Check before acting: `if can_harvest()` before `harvest()`
- Power from sunflowers = 2x movement speed
- Avoid adjacent trees (they slow each other)
- Water pumpkins for faster growth

## Known Gotchas

1. `Entities.Hay` doesn't exist - use `Entities.Grass` (yields hay)
2. Workers can't return values - must scan after they finish
3. Pumpkin harvest() on one triggers all connected
4. Sunflower bonus is lost if you harvest wrong order
5. `till()` toggles - calling twice returns to grassland
6. Dead pumpkins exist but can't be harvested
7. Maze `measure()` works from anywhere inside maze
