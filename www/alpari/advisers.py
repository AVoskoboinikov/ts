from find_unicorns import findUnicorns
from get_unicorn_index import getUnicornIndex

def alwaysTrue(historyData):
	return True

def alwaysFalse(historyData):
	return False

def adviserThreeSteps(historyData):
	ok = False
	
	# find bottom points where graph changes direction
	up, down = findUnicorns(historyData[-10:])
	
	# check if previous points are like steps
	if down == sorted(down) and len(down) >= 3:
		ok = True
		
		# checks that previous points are not lying in horizontal line
		for i in range(1, len(down)):
			if abs(down[i] - down[i-1]) == 0:
				ok = False
		
		if ok:
			up, down = findUnicorns(historyData)
			
			# check if previos graph moving down
			if down == sorted(down, reverse=True):
				ok = False

		if ok:
			up, down = getUnicornIndex(historyData)

			# check that previous graph moves more up, then down
			if down > up or abs(up - down) <= 0.0001 or abs(up - down) >= 0.0005:
				ok = False

			if up >= 0.002:
				ok = False

			if down >= 0.0015:
				ok = False

		if ok:
			up, down = findUnicorns(historyData[-10:])
			sortedUp = sorted(up)
			sortedDown = sorted(down)

			# checks that distance between each step is not too big
			if len(sortedDown) > 0 and len(sortedUp) > 0:
				x1 = sortedDown[0]
				x2 = sortedUp[-1]

				if abs(x2 - x1) >= 0.0001:
					ok = False

	return ok
	