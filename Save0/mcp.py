import logs

logs.log("=== GOLD SIM (10x10 to 10M) ===")
time = simulate("sim_gold", Unlocks, {Items.Power: 100000000, Items.Weird_Substance: 100000000}, {}, 42, 100)
logs.log("Total time: " + str(time) + "s")
