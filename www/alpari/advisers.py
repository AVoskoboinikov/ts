from find_unicorns import findUnicorns
from get_unicorn_index import getUnicornIndex
from trend import trendEMA, isTrendMovingUp, isTrendMovingDown
from volatility import getVolatility, getUpVolatility, getDownVolatility
from helpers import getTrendGraphPierceIndex, getTrendGraphPierceWeightedIndex, getTrendGraphUnPierceWeightedIndex


def alwaysTrue(historyData):
	return True

def alwaysFalse(historyData):
	return False

def adviserThreeSteps(historyData):
	ok = False
	unicornWindow = 10

	# find bottom points where graph changes direction
	up, down = findUnicorns(historyData[-unicornWindow:])
	
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
			up, down = findUnicorns(historyData[-unicornWindow:])
			sortedUp = sorted(up)
			sortedDown = sorted(down)

			# checks that distance between each step is not too big
			if len(sortedDown) > 0 and len(sortedUp) > 0:
				x1 = sortedDown[0]
				x2 = sortedUp[-1]

				if abs(x2 - x1) >= 0.0001:
					ok = False

	return ok

def adviserTrendUp(historyData):
	windowToCheck = 150
	totalWindowToCheck = 300

	sampleTicks = historyData[-windowToCheck:]
	totalPrevTicks = historyData[-windowToCheck-totalWindowToCheck : -windowToCheck]

	isOK = False

	emaTrend = trendEMA(sampleTicks, 5, 0.2)
	trendUp = isTrendMovingUp(emaTrend, 10)

	emaTotalTrend = trendEMA(totalPrevTicks, 25, 0.2) # 25, 0.2
	totalTrendDown = isTrendMovingDown(emaTotalTrend, 35) # 35
	totalTrendUp = isTrendMovingUp(emaTotalTrend, 35)

	# sampleVolatility, sampleMaxVolatility = getVolatility(sampleTicks)
	sampleUpVolatility, sampleUpMaxVolatility = getUpVolatility(sampleTicks)
	# sampleDownVolatility, sampleDownMaxVolatility = getDownVolatility(sampleTicks)

	# totalUp, totalDown = getUnicornIndex(sampleTicks)
	# totalUp = round(totalUp, 4)
	# totalDown = round(totalDown, 4)

	# piercedUpIndex = getTrendGraphPierceWeightedIndex(emaTotalTrend, totalPrevTicks)
	# piercedDownIndex = getTrendGraphUnPierceWeightedIndex(emaTotalTrend, totalPrevTicks)

	if trendUp:
		isOK = True

	if isOK:
		isOK = False

		subTrendWindow = 75
		subTrendTicks = historyData[-subTrendWindow:]
		emaSubTrend = trendEMA(subTrendTicks, 4, 0.4)
		subTrendUp = isTrendMovingUp(emaSubTrend, 10)

		if subTrendUp:
			isOK = True

	if isOK and totalTrendDown:
		isOK = False

		if min(emaTotalTrend) > max(emaTrend):
			isOK = True

	if isOK:
		isOK = False

		if sampleUpVolatility < 0.00015:
			isOK = True

	return isOK
	