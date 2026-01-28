import logs

logs.log("=== CACTUS SIM (until 10M) ===")
time = simulate("sim_cactus", Unlocks, {Items.Power: 100000000, Items.Pumpkin: 100000000}, {}, 42, 100)
logs.log("Done in " + str(time) + "s real time")
