import pandas as pd

from find_unicorns import findUnicorns
from get_unicorn_index import getUnicornIndex
from trend import trendEMA, isTrendMovingUp, isTrendMovingUp2, isTrendMovingDown, isTrendMovingDown2
from volatility import getVolatility, getUpVolatility, getDownVolatility
from helpers import getTrendGraphPierceIndex, getTrendGraphPierceWeightedIndex, getTrendGraphUnPierceWeightedIndex, linesNotCross


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


def getAdditionalData(ticks):
	subTrendTicks = ticks[-75 : ]
	trendTicks = ticks[-150 : ]
	totalTrendTicks = ticks[-450 : -150]

	emaSubTrend = trendEMA(subTrendTicks, 4, 0.4)
	emaTrend = trendEMA(trendTicks, 5, 0.2)
	emaTotalTrend = trendEMA(totalTrendTicks, 25, 0.2)

	_, volatility1Max, _ = getVolatility(trendTicks, 1)
	_, volatility3Max, _ = getVolatility(trendTicks, 3)

	return {
		'sub-trend': {'trend': emaSubTrend},
		'main-trend': {'trend': emaTrend},
		'total-trend': {'trend': emaTotalTrend},
		'volatility-1-max': round(volatility1Max, 5),
		'volatility-3-max': round(volatility3Max, 5),
	}

def adviserAudNzdCommonPattern(audTicks, nzdTicks):
	audData = getAdditionalData(audTicks)
	nzdData = getAdditionalData(nzdTicks)

	isOk = False

	audFPoint = audData['total-trend']['trend'][0]
	audLPoint = audData['total-trend']['trend'][-1]
	audFPoint1 = audData['main-trend']['trend'][0]
	audLPoint1 = audData['main-trend']['trend'][-1]
	audFPoint2 = audData['sub-trend']['trend'][0]
	audLPoint2 = audData['sub-trend']['trend'][-1]

	nzdFPoint = nzdData['total-trend']['trend'][0]
	nzdLPoint = nzdData['total-trend']['trend'][-1]
	nzdFPoint1 = nzdData['main-trend']['trend'][0]
	nzdLPoint1 = nzdData['main-trend']['trend'][-1]
	nzdFPoint2 = nzdData['sub-trend']['trend'][0]
	nzdLPoint2 = nzdData['sub-trend']['trend'][-1]


	# перевірка, що між графіками ауд і нсд зберігаєтсья картинка того, як розташовані тренди

	# перші точки головного і суб тренда менші за останню точку повного тренда
	# останні точки головного і суб тренда більші за останню точку повного тренда
	if audLPoint > audFPoint1 and audLPoint > audFPoint2 and audLPoint < audLPoint1 and audLPoint < audLPoint2:
		if nzdLPoint > nzdFPoint1 and nzdLPoint > nzdFPoint2 and nzdLPoint < nzdLPoint1 and nzdLPoint < nzdLPoint2:
			isOk = True

	# перша точка головного тренда менша за останню точку повного тренда
	# перша точка суб тренда більша за останню точку повного тренда
	# останні точки головного і суб тренда більші за останню точку повного тренда
	if audLPoint > audFPoint1 and audLPoint < audFPoint2 and audLPoint < audLPoint1 and audLPoint < audLPoint2:
		if nzdLPoint > nzdFPoint1 and nzdLPoint < nzdFPoint2 and nzdLPoint < nzdLPoint1 and nzdLPoint < nzdLPoint2:
			isOk = True

	if audLPoint < audFPoint1 and audLPoint < audFPoint2 and audLPoint < audLPoint1 and audLPoint < audLPoint2:
		if nzdLPoint < nzdFPoint1 and nzdLPoint < nzdFPoint2 and nzdLPoint < nzdLPoint1 and nzdLPoint < nzdLPoint2:
			isOk = True

	if isOk:
		if not linesNotCross(audData['sub-trend']['trend'], audData['main-trend']['trend'][-75:]):
			isOk = False

		if not linesNotCross(nzdData['sub-trend']['trend'], nzdData['main-trend']['trend'][-75:]):
			isOk = False

	if isOk:
		volatilityLimit = 0.001

		if audData['volatility-1-max'] >= volatilityLimit or nzdData['volatility-1-max'] >= volatilityLimit:
			isOk = False

		if audData['volatility-3-max'] >= volatilityLimit or nzdData['volatility-3-max'] >= volatilityLimit:
			isOk = False

	# if isOk:
	# 	isOk = False

	# 	if audLPoint > audFPoint and nzdLPoint > nzdFPoint:
	# 		isOk = True

	# 	if audLPoint < audFPoint and nzdLPoint < nzdFPoint:
	# 		isOk = True

	return isOk

def getCorr(corrFrom, corrTo):
	corr = 0

	df = pd.DataFrame.from_items([('corrFrom', corrFrom), ('corrTo', corrTo)])
	corr = df.corr()

	return corr['corrFrom']['corrTo']

def adviserCorrelation(audUsdTicks, usdZarTicks, nzdUsdTicks, eurNzdTicks):
	AudUsdNzdUsdCorr = getCorr(audUsdTicks, nzdUsdTicks)
	AudUsdUsdZarCorr = getCorr(audUsdTicks, usdZarTicks)
	NzdUsdEurNzdCorr = getCorr(nzdUsdTicks, eurNzdTicks)

	resultAction = 0 # do nothing

	if AudUsdNzdUsdCorr < -0.7 and AudUsdUsdZarCorr > 0.5 and NzdUsdEurNzdCorr < -0.5:
		# emaAudUsdTrend = trendEMA(audUsdTicks, 2, 0.1)
		emaAudUsdTrendUp = isTrendMovingUp2(audUsdTicks)
		emaAudUsdTrendDown = isTrendMovingDown2(audUsdTicks)

		# emaNzdUsdTrend = trendEMA(nzdUsdTicks, 2, 0.1)
		emaNzdUsdTrendUp = isTrendMovingUp2(nzdUsdTicks)
		emaNzdUsdTrendDown = isTrendMovingDown2(nzdUsdTicks)
		
		if emaAudUsdTrendUp and emaNzdUsdTrendDown:
			resultAction = -1 # sell

		if emaAudUsdTrendDown and emaNzdUsdTrendUp:
			resultAction = 1 # buy

	return resultAction