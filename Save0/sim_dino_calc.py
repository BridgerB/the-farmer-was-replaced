import logs

def calc_move_ticks(apples_eaten):
	ticks = 400
	for i in range(apples_eaten):
		ticks = ticks - (ticks * 3) // 100
	return ticks

def calc_total_ticks(num_apples):
	total = 0
	ticks = 400
	for i in range(num_apples):
		total = total + ticks
		ticks = ticks - (ticks * 3) // 100
	return total

def cycle():
	logs.log("=== DINO THEORETICAL ANALYSIS ===")
	logs.log("")
	logs.log("Bones = apples^2")
	logs.log("Move ticks: 400 base, -3% per apple")
	logs.log("")

	for size in [3, 5, 7, 10, 15, 22]:
		apples = size * size
		bones = apples * apples
		moves_needed = apples
		ticks = calc_total_ticks(apples)
		ratio = (bones * 1000000) // ticks
		logs.log("Size " + str(size) + ": " + str(apples) + " apples, " + str(bones) + " bones, " + str(ticks) + " ticks, ratio=" + str(ratio))

	logs.log("")
	logs.log("Move ticks after X apples:")
	for n in [0, 10, 25, 50, 100, 200, 400]:
		t = calc_move_ticks(n)
		logs.log("  " + str(n) + " apples: " + str(t) + " ticks/move")

	logs.log("")
	logs.log("=== CONCLUSION ===")
	logs.log("Larger worlds give better bones/tick because:")
	logs.log("1. bones scale as N^4 (apples^2 = (N^2)^2)")
	logs.log("2. ticks scale as ~N^2 (one move per apple)")
	logs.log("3. move cost decreases as you eat more apples")
	logs.log("")
	logs.log("Best ratio: largest world you can fully complete")
	