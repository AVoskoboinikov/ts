import pandas as pd
import matplotlib.pyplot as plt
import math

from find_unicorns import findUnicorns
from get_unicorn_index import getUnicornIndex
from trend import trendEMA, isTrendMovingUp, isTrendMovingDown
from volatility import getVolatility, getUpVolatility, getDownVolatility
from helpers import getTrendGraphPierceIndex, getTrendGraphPierceWeightedIndex, getTrendGraphUnPierceWeightedIndex, linesNotCross

from advisers import adviserTrendUp

windowToCheck = 450
afterLag = 200


def isPositiveFixture(ticks):
	isOk = False
	
	for i in range(len(ticks)):
		if (ticks[i] - ticks[0]) > 0.001:
			isOk = True

		if (ticks[0] - ticks[i]) > 0.001:
			return False 

	return isOk

def addAdditionalInfoToPlot(info):
	# sub-trend
	y_axis = [float(tick) for tick in info['mini-trend']['trend']]
	x_axis = info['mini-trend']['x']
	plt.plot(x_axis, y_axis, 'r-')

	# sub-trend
	y_axis = [float(tick) for tick in info['sub-trend']['trend']]
	x_axis = info['sub-trend']['x']
	plt.plot(x_axis, y_axis, 'b-')

	# main-trend
	y_axis = [float(tick) for tick in info['main-trend']['trend']]
	x_axis = info['main-trend']['x']
	plt.plot(x_axis, y_axis, 'm-')
	
	# total-trend
	y_axis = [float(tick) for tick in info['total-trend']['trend']]
	x_axis = info['total-trend']['x']
	plt.plot(x_axis, y_axis, 'k-')

	plt.figtext(0.025, 0.975, "Volatility1: " + str(format(info['volatility-1'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.025, 0.95, "mVolatility1: " + str(format(info['volatility-1-max'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.025, 0.925, "countMV: " + str(len(info['volatility-1-series'])), color="black", weight=500, size="medium")

	plt.figtext(0.175, 0.975, "Volatility3: " + str(format(info['volatility-3'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.175, 0.95, "mVolatility3: " + str(format(info['volatility-3-max'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.175, 0.925, "countMV: " + str(len(info['volatility-3-series'])), color="black", weight=500, size="medium")


def drawPlot(plotTitle, ticksToDraw, additionalData):
	y_axis = [float(tick) for tick in ticksToDraw]
	x_axis = [i for i in range(1, len(ticksToDraw) + 1)]

	fig = plt.figure()
	fig.set_size_inches(15,8)
	fig.canvas.set_window_title(plotTitle)

	plt.plot(x_axis, y_axis, 'g-')
	plt.ylabel(plotTitle)
	plt.axvline(windowToCheck)

	addAdditionalInfoToPlot(additionalData)

	plt.grid()

	# plt.show()
	plt.savefig('../plots/hypothesis/' + plotTitle + '.png')

	plt.clf()
	plt.close(fig)



def drawAudPlot(currentTick, ticksToDraw, additionalData):
	plotTitle = str(currentTick) + '_aud'
	drawPlot(plotTitle, ticksToDraw, additionalData)

def drawNzdPlot(currentTick, ticksToDraw, additionalData):
	plotTitle = str(currentTick) + '_nzd'
	drawPlot(plotTitle, ticksToDraw, additionalData)




def getAdditionalData(ticks):
	miniTrendTicks = ticks[-20 : ]
	subTrendTicks = ticks[-75 : ]
	trendTicks = ticks[-150 : ]
	totalTrendTicks = ticks[-450 : -150]

	emaMiniTrend = trendEMA(miniTrendTicks, 2, 0.1)
	emaSubTrend = trendEMA(subTrendTicks, 4, 0.4)
	emaTrend = trendEMA(trendTicks, 5, 0.2)
	emaTotalTrend = trendEMA(totalTrendTicks, 25, 0.2)

	volatility1, volatility1Max, volatility1Series = getVolatility(trendTicks, 1)
	volatility3, volatility3Max, volatility3Series = getVolatility(trendTicks, 3)

	return {
		'mini-trend': {'trend': emaMiniTrend, 'x': range(windowToCheck - len(emaMiniTrend) + 1, windowToCheck + 1)},
		'sub-trend': {'trend': emaSubTrend, 'x': range(windowToCheck - len(subTrendTicks) + 1, windowToCheck + 1)},
		'main-trend': {'trend': emaTrend, 'x': range(windowToCheck - len(emaTrend) + 1, windowToCheck + 1)},
		'total-trend': {'trend': emaTotalTrend, 'x': range(windowToCheck - len(trendTicks) - len(emaTotalTrend) + 1, windowToCheck - len(trendTicks) + 1)},
		'volatility-1': round(volatility1, 5),
		'volatility-1-max': round(volatility1Max, 5),
		'volatility-1-series': volatility1Series,
		'volatility-3': round(volatility3, 5),
		'volatility-3-max': round(volatility3Max, 5),
		'volatility-3-series': volatility3Series,
	}

def checkIfStartToFall(ticks):
	for i in range(15, 50):
		subTicks = ticks[-i:]
		trend = trendEMA(subTicks, 2, 0.1)

		if (trend == sorted(trend, reverse=True)) and abs(subTicks[0] - subTicks[-1]) >= 0.0003:
			return True

	return False

def getAudAndNzdTicks():
	fileToReadAUD = 'AUDUSD1M - last year.csv'
	# fileToRead = 'AUDUSD1M.csv'
	
	fileToReadNZD = 'NZDUSD1M - last year.csv'
	# fileToRead = 'NZDUSD1M.csv'

	audusd = pd.read_csv(fileToReadAUD, usecols=['Date', 'Time', 'Open'])
	audusd.rename(columns={'Open':'Open AUDUSD'}, inplace=True)
	audusd['Date Time'] = audusd['Date'].map(str) + ':' + audusd['Time'].map(str)
	audusd.set_index('Date Time', inplace=True)
	del audusd['Date']
	del audusd['Time']

	nzdusd = pd.read_csv(fileToReadNZD, usecols=['Date', 'Time', 'Open'])
	nzdusd.rename(columns={'Open':'Open NZDUSD'}, inplace=True)
	nzdusd['Date Time'] = nzdusd['Date'].map(str) + ':' + nzdusd['Time'].map(str)
	nzdusd.set_index('Date Time', inplace=True)
	del nzdusd['Date']
	del nzdusd['Time']

	audnzd = audusd.join(nzdusd, how='inner')
	audnzd.reset_index(inplace=True)

	del audusd
	del nzdusd

	return audnzd['Open AUDUSD'].values, audnzd['Open NZDUSD'].values

openAudUsd, openNzdUsd = getAudAndNzdTicks()

ticksStep = 1
skipTicks = 0

for tick in range(windowToCheck, len(openNzdUsd), ticksStep):

	if skipTicks > 0:
		skipTicks -= 1
		continue

	sampleAudUsdTicks = openAudUsd[tick-windowToCheck+1 : tick+1]
	sampleNzdUsdTicks = openNzdUsd[tick-windowToCheck+1 : tick+1]

	isNzdOk = adviserTrendUp(sampleNzdUsdTicks)
	# isAudOk = adviserTrendUp(sampleAudUsdTicks)

	isOk = isNzdOk
	
	if isOk:
		skipTicks = 30

		audData = getAdditionalData(sampleAudUsdTicks)
		nzdData = getAdditionalData(sampleNzdUsdTicks)

		# if isOk:
		# 	# must be used
		# 	nzdFPoint = nzdData['total-trend']['trend'][0]
		# 	nzdLPoint = nzdData['total-trend']['trend'][-1]

		# 	audFPoint = audData['total-trend']['trend'][0]
		# 	audLPoint = audData['total-trend']['trend'][-1]
			
		# 	if ((nzdFPoint > nzdLPoint) and abs(nzdFPoint-nzdLPoint) >= 0.0005) and ((audFPoint > audLPoint) and abs(audFPoint-audLPoint) >= 0.0005):
		# 		audLPoint1 = audData['total-trend']['trend'][-1]
		# 		audLPoint2 = audData['main-trend']['trend'][-1]

		# 		nzdLPoint1 = nzdData['total-trend']['trend'][-1]
		# 		nzdLPoint2 = nzdData['main-trend']['trend'][-1]

		# 		if audLPoint1 > audLPoint2 and nzdLPoint1 > nzdLPoint2:
		# 			isOk = False

		# if isOk:
		# 	if checkIfStartToFall(sampleAudUsdTicks) or checkIfStartToFall(sampleNzdUsdTicks):
		# 		isOk = False
		
		if isOk:
			isOk = False

			audLPoint = audData['total-trend']['trend'][-1]
			audFPoint1 = audData['main-trend']['trend'][0]
			audLPoint1 = audData['main-trend']['trend'][-1]
			audFPoint2 = audData['sub-trend']['trend'][0]
			audLPoint2 = audData['sub-trend']['trend'][-1]

			nzdLPoint = nzdData['total-trend']['trend'][-1]
			nzdFPoint1 = nzdData['main-trend']['trend'][0]
			nzdLPoint1 = nzdData['main-trend']['trend'][-1]
			nzdFPoint2 = nzdData['sub-trend']['trend'][0]
			nzdLPoint2 = nzdData['sub-trend']['trend'][-1]


			# перевірка, що між графіками ауд і нсд зберігаєтсья картинка того, як розташовані тренди

			# перші точки головного і суб тренда менші за останню точку повного тренда
			# останні точки головного і суб тренда більші за останню точку повного тренда
			# if audLPoint > audFPoint1 and audLPoint > audFPoint2 and audLPoint < audLPoint1 and audLPoint < audLPoint2:
			# 	if nzdLPoint > nzdFPoint1 and nzdLPoint > nzdFPoint2 and nzdLPoint < nzdLPoint1 and nzdLPoint < nzdLPoint2:
			# 		isOk = True

			# перша точка головного тренда менша за останню точку повного тренда
			# перша точка суб тренда більша за останню точку повного тренда
			# останні точки головного і суб тренда більші за останню точку повного тренда
			if audLPoint > audFPoint1 and audLPoint < audFPoint2 and audLPoint < audLPoint1 and audLPoint < audLPoint2:
				if nzdLPoint > nzdFPoint1 and nzdLPoint < nzdFPoint2 and nzdLPoint < nzdLPoint1 and nzdLPoint < nzdLPoint2:
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

		# 	audMiniTrend = audData['mini-trend']['trend']
		# 	nzdMiniTrend = nzdData['mini-trend']['trend']

		# 	if audMiniTrend == sorted(audMiniTrend, reverse=True) or nzdMiniTrend == sorted(nzdMiniTrend, reverse=True):
		# 		isOk = True

		# if isOk:
			# isOk = not isPositiveFixture(openNzdUsd[tick : tick+afterLag+1])

	if isOk:
		audTicksToDraw = openAudUsd[tick-windowToCheck : tick+afterLag+1]
		nzdTicksToDraw = openNzdUsd[tick-windowToCheck : tick+afterLag+1]

		drawAudPlot(tick, audTicksToDraw, audData)
		drawNzdPlot(tick, nzdTicksToDraw, nzdData)



# don't know how to use:

# if isOk:
	# 	# isOk = False

	# 	# must be used
	# 	# якщо повний тренд nzd падає, але aud тренд при цьому зріс трохи - це ок
	# 	fPoint = audData['total-trend']['trend'][0]
	# 	lPoint = audData['total-trend']['trend'][-1]
	# 	if (fPoint < lPoint) and abs(fPoint - lPoint) >= 0.0001:
	# 		isOk = True

	# 	if not isOk:
	# 		audLPoint = audData['total-trend']['trend'][-1]
	# 		audFPoint1 = audData['main-trend']['trend'][0]
	# 		audLPoint1 = audData['main-trend']['trend'][-1]
	# 		audFPoint2 = audData['sub-trend']['trend'][0]
	# 		audLPoint2 = audData['sub-trend']['trend'][-1]

	# 		nzdLPoint = nzdData['total-trend']['trend'][-1]
	# 		nzdFPoint1 = nzdData['main-trend']['trend'][0]
	# 		nzdLPoint1 = nzdData['main-trend']['trend'][-1]
	# 		nzdFPoint2 = nzdData['sub-trend']['trend'][0]
	# 		nzdLPoint2 = nzdData['sub-trend']['trend'][-1]


	# 		# перевірка, що між графіками ауд і нсд зберігаєтсья картинка того, як розташовані тренди

	# 		# перші точки головного і суб тренда менші за останню точку повного тренда
	# 		# останні точки головного і суб тренда більші за останню точку повного тренда
	# 		if audLPoint > audFPoint1 and audLPoint > audFPoint2 and audLPoint < audLPoint1 and audLPoint < audLPoint2:
	# 			if nzdLPoint > nzdFPoint1 and nzdLPoint > nzdFPoint2 and nzdLPoint < nzdLPoint1 and nzdLPoint < nzdLPoint2:
	# 				isOk = True

	# 		# перша точка головного тренда менша за останню точку повного тренда
	# 		# перша точка суб тренда більша за останню точку повного тренда
	# 		# останні точки головного і суб тренда більші за останню точку повного тренда
	# 		if audLPoint > audFPoint1 and audLPoint < audFPoint2 and audLPoint < audLPoint1 and audLPoint < audLPoint2:
	# 			if nzdLPoint > nzdFPoint1 and nzdLPoint < nzdFPoint2 and nzdLPoint < nzdLPoint1 and nzdLPoint < nzdLPoint2:
	# 				isOk = True