from find_unicorns import findUnicorns
from get_unicorn_index import getUnicornIndex

def alwaysTrue(historyData):
	return True

def alwaysFalse(historyData):
	return False

def advicerThreeSteps(historyData):
	ok = False
	
	up, down = findUnicorns(historyData[-10:])
	
	if down == sorted(down) and len(down) >= 3:
		ok = True
		
		# maybe this block can be deleted
		for i in range(1, len(down)):
			if abs(down[i] - down[i-1]) == 0:
				ok = False
		
		if ok:
			up, down = findUnicorns(historyData[-50: -10])
			
			if down == sorted(down, reverse=True):
				ok = False

		if ok:
			up, down = getUnicornIndex(historyData[-50: -10])

			if down > up or abs(up - down) < 0.0002:
				ok = False

		if ok:
			up, down = findUnicorns(historyData[-10:])
			sortedUp = sorted(up)
			sortedDown = sorted(down)

			if len(sortedDown) > 0 and len(sortedUp) > 0:
				x1 = sortedDown[0]
				x2 = sortedUp[-1]

				if abs(x2 - x1) >= 0.0001:
					ok = False

	return ok
	