import logs

logs.log("=== BONE SIM SEED TEST ===")
for seed in range(5):
	time = simulate("sim_bone", Unlocks, {Items.Power: 100000000, Items.Cactus: 100000000}, {}, seed, 100)
	logs.log("Seed " + str(seed) + ": " + str(time) + "s")
