import logs

logs.log("=== BONE SIM (until 10M) ===")
time = simulate("sim_bone", Unlocks, {Items.Power: 100000000, Items.Cactus: 100000000}, {}, 42, 100)
logs.log("Done in " + str(time) + "s real time")
