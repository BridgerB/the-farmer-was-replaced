import logs

logs.log("=== HAY SIM (until 10M) ===")
time = simulate("sim_hay", Unlocks, {Items.Power: 100000000}, {}, 42, 100)
logs.log("Done in " + str(time) + "s real time")
