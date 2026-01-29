import logs

logs.log("=== GOLD SIM (32x32 MAX DRONES) ===")
time = simulate("sim_gold", Unlocks, {Items.Power: 100000000, Items.Weird_Substance: 100000000}, {}, 42, 1500)
logs.log("Total time: " + str(time) + "s")
