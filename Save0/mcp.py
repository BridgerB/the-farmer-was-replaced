import logs

logs.log("=== WOOD SIM (until 10M) ===")
time = simulate("sim_wood", Unlocks, {Items.Power: 100000000}, {}, 42, 100)
logs.log("Done in " + str(time) + "s real time")
