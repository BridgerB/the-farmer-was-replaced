import logs

logs.log("=== CARROT SIM (until 10M) ===")
time = simulate("sim_carrot", Unlocks, {Items.Power: 100000000, Items.Wood: 100000000, Items.Hay: 100000000}, {}, 42, 100)
logs.log("Done in " + str(time) + "s real time")
