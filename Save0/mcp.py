import logs

logs.log("=== POWER FARMING (PARALLEL + WATER) ===")
time = simulate("sim_power", Unlocks, {Items.Carrot: 100000000, Items.Water: 100000000, Items.Power: 10000}, {}, 42, 1500)
logs.log("Total sim time: " + str(time) + "s")
