import logs

logs.log("Running dino simulation at max speed...")

time = simulate("test_dino", Unlocks, {Items.Cactus: 10000000}, {}, 0, 100000)

logs.log("Simulation finished in " + str(time) + " seconds")
