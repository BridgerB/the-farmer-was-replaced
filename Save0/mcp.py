import logs

logs.log("=== WEIRD SUBSTANCE SIM ===")
time = simulate("sim_weird", Unlocks, {Items.Power: 100000000, Items.Fertilizer: 100000000}, {}, 42, 100)
logs.log("Sim time: " + str(time) + "s")
