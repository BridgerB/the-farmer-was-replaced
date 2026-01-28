import logs

logs.log("=== HAY SIM (until 10M) ===")
time = simulate("mcp_sim", Unlocks, {}, {}, 0, 100)
logs.log("Done in " + str(time) + "s real time")
