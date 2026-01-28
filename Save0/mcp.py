import logs

logs.log("=== PUMPKIN SIM (until 10M) ===")
time = simulate("sim_pumpkin", Unlocks, {Items.Power: 100000000, Items.Carrot: 100000000, Items.Water: 100000000}, {}, 42, 100)
logs.log("Done in " + str(time) + "s real time")
