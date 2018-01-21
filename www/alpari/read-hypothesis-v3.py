import pandas as pd
import matplotlib.pyplot as plt
import math

from find_unicorns import findUnicorns
from get_unicorn_index import getUnicornIndex
from trend import trendEMA, isTrendMovingUp, isTrendMovingUp2, isTrendMovingDown, isTrendMovingDown2
from volatility import getVolatility, getUpVolatility, getDownVolatility
from helpers import getTrendGraphPierceIndex, getTrendGraphPierceWeightedIndex, getTrendGraphUnPierceWeightedIndex, linesNotCross

from advisers import adviserTrendUp, adviserAudNzdCommonPattern, adviserCorrelation

windowToCheck = 450
afterLag = 200

def getCorr(corrFrom, corrTo):
	corr = 0

	df = pd.DataFrame.from_items([('corrFrom', corrFrom), ('corrTo', corrTo)])
	corr = df.corr()

	return corr['corrFrom']['corrTo']

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

	# # sub-trend
	# y_axis = [float(tick) for tick in info['sub-trend']['trend']]
	# x_axis = info['sub-trend']['x']
	# plt.plot(x_axis, y_axis, 'b-')

	# # main-trend
	# y_axis = [float(tick) for tick in info['main-trend']['trend']]
	# x_axis = info['main-trend']['x']
	# plt.plot(x_axis, y_axis, 'm-')
	
	# # total-trend
	# y_axis = [float(tick) for tick in info['total-trend']['trend']]
	# x_axis = info['total-trend']['x']
	# plt.plot(x_axis, y_axis, 'k-')

	plt.figtext(0.025, 0.975, "AudUsd-NzdUsd Corr: " + str(format(info['AudUsd-NzdUsd Corr'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.025, 0.95, "AudUsd-UsdZar Corr: " + str(format(info['AudUsd-UsdZar Corr'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.025, 0.925, "NzdUsd-EurNzd Corr: " + str(format(info['NzdUsd-EurNzd Corr'], 'f')), color="black", weight=500, size="medium")

	plt.figtext(0.325, 0.975, "Up: " + str(format(info['mini-trend-up'], 'f')), color="black", weight=500, size="medium")	
	plt.figtext(0.325, 0.95, "Down: " + str(format(info['mini-trend-down'], 'f')), color="black", weight=500, size="medium")	

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



def drawAudUsdPlot(currentTick, ticksToDraw, additionalData):
	plotTitle = str(currentTick) + '_aud-usd'
	drawPlot(plotTitle, ticksToDraw, additionalData)

def drawNzdUsdPlot(currentTick, ticksToDraw, additionalData):
	plotTitle = str(currentTick) + '_nzd-usd'
	drawPlot(plotTitle, ticksToDraw, additionalData)

def drawUsdZarPlot(currentTick, ticksToDraw, additionalData):
	plotTitle = str(currentTick) + '_usd-zar'
	drawPlot(plotTitle, ticksToDraw, additionalData)

def drawEurNzdPlot(currentTick, ticksToDraw, additionalData):
	plotTitle = str(currentTick) + '_eur-nzd'
	drawPlot(plotTitle, ticksToDraw, additionalData)



def getAdditionalData(ticks):
	miniTrendTicks = ticks[-30 : ]
	# subTrendTicks = ticks[-75 : ]
	# trendTicks = ticks[-150 : ]
	# totalTrendTicks = ticks[-450 : -150]

	emaMiniTrend = trendEMA(miniTrendTicks, 2, 0.1)
	# emaSubTrend = trendEMA(subTrendTicks, 4, 0.4)
	# emaTrend = trendEMA(trendTicks, 5, 0.2)
	# emaTotalTrend = trendEMA(totalTrendTicks, 25, 0.2)

	return {
		'mini-trend': {'trend': emaMiniTrend, 'x': range(windowToCheck - len(emaMiniTrend) + 1, windowToCheck + 1)},
		'mini-trend-up': isTrendMovingUp2(miniTrendTicks),
		'mini-trend-down': isTrendMovingDown2(miniTrendTicks),
		# 'sub-trend': {'trend': emaSubTrend, 'x': range(windowToCheck - len(subTrendTicks) + 1, windowToCheck + 1)},
		# 'main-trend': {'trend': emaTrend, 'x': range(windowToCheck - len(emaTrend) + 1, windowToCheck + 1)},
		# 'total-trend': {'trend': emaTotalTrend, 'x': range(windowToCheck - len(trendTicks) - len(emaTotalTrend) + 1, windowToCheck - len(trendTicks) + 1)},
	}

def checkIfStartToFall(ticks):
	for i in range(15, 50):
		subTicks = ticks[-i:]
		trend = trendEMA(subTicks, 2, 0.1)

		if (trend == sorted(trend, reverse=True)) and abs(subTicks[0] - subTicks[-1]) >= 0.0003:
			return True

	return False

def readFile(FileName, pair):
	data = pd.read_csv(FileName, usecols=['Date', 'Time', 'Open'])
	data.rename(columns={'Open':'Open ' + pair}, inplace=True)
	data['Date Time'] = data['Date'].map(str) + ':' + data['Time'].map(str)
	data.set_index('Date Time', inplace=True)
	del data['Date']
	del data['Time']

	return data

def getAudAndNzdTicks():
	fileToReadAUD = 'AUDUSD1M - last year.csv'
	fileToReadAUD2 = 'USDZAR1M - last year.csv'
	
	fileToReadNZD = 'NZDUSD1M - last year.csv'
	fileToReadNZD2 = 'EURNZD1M - last year.csv'

	audusd = readFile(fileToReadAUD, 'AUDUSD')
	usdzar = readFile(fileToReadAUD2, 'USDZAR')

	nzdusd = readFile(fileToReadNZD, 'NZDUSD')
	eurnzd = readFile(fileToReadNZD2, 'EURNZD')

	joined = audusd.join(usdzar, how='inner')
	joined = joined.join(nzdusd, how='inner')
	joined = joined.join(eurnzd, how='inner')
	joined.reset_index(inplace=True)

	return joined['Open AUDUSD'].values, joined['Open USDZAR'].values, joined['Open NZDUSD'].values, joined['Open EURNZD'].values

print("init")

openAudUsd, openUsdZar, openNzdUsd, openEurNzd = getAudAndNzdTicks()

print("loaded")

ticksStep = 1
skipTicks = 0

for tick in range(windowToCheck, len(openNzdUsd), ticksStep):
	period = 30

	if skipTicks > 0:
		skipTicks -= 1
		continue

	sampleAudUsdTicks = openAudUsd[tick-windowToCheck+1 : tick+1]
	sampleUsdZarTicks = openUsdZar[tick-windowToCheck+1 : tick+1]
	sampleNzdUsdTicks = openNzdUsd[tick-windowToCheck+1 : tick+1]
	sampleEurNzdTicks = openEurNzd[tick-windowToCheck+1 : tick+1]

	isOk = adviserCorrelation(sampleAudUsdTicks[-period : ], sampleUsdZarTicks[-period : ], sampleNzdUsdTicks[-period : ], sampleEurNzdTicks[-period : ])

	if isOk == 1 or isOk == -1:
		skipTicks = 30

		AudUsdNzdUsdCorr = getCorr(sampleAudUsdTicks[-period : ], sampleNzdUsdTicks[-period : ])
		AudUsdUsdZarCorr = getCorr(sampleAudUsdTicks[-period : ], sampleUsdZarTicks[-period : ])
		NzdUsdEurNzdCorr = getCorr(sampleNzdUsdTicks[-period : ], sampleEurNzdTicks[-period : ])

		AudUsdData = getAdditionalData(sampleAudUsdTicks)
		UsdZarData = getAdditionalData(sampleUsdZarTicks)
		NzdUsdData = getAdditionalData(sampleNzdUsdTicks)
		EurNzdData = getAdditionalData(sampleEurNzdTicks)

		AudUsdData['AudUsd-NzdUsd Corr'] = AudUsdNzdUsdCorr
		AudUsdData['AudUsd-UsdZar Corr'] = AudUsdUsdZarCorr
		AudUsdData['NzdUsd-EurNzd Corr'] = NzdUsdEurNzdCorr

		UsdZarData['AudUsd-NzdUsd Corr'] = AudUsdNzdUsdCorr
		UsdZarData['AudUsd-UsdZar Corr'] = AudUsdUsdZarCorr
		UsdZarData['NzdUsd-EurNzd Corr'] = NzdUsdEurNzdCorr

		NzdUsdData['AudUsd-NzdUsd Corr'] = AudUsdNzdUsdCorr
		NzdUsdData['AudUsd-UsdZar Corr'] = AudUsdUsdZarCorr
		NzdUsdData['NzdUsd-EurNzd Corr'] = NzdUsdEurNzdCorr

		EurNzdData['AudUsd-NzdUsd Corr'] = AudUsdNzdUsdCorr
		EurNzdData['AudUsd-UsdZar Corr'] = AudUsdUsdZarCorr
		EurNzdData['NzdUsd-EurNzd Corr'] = NzdUsdEurNzdCorr

	if isOk == 1 or isOk == -1:
		AudUsdTicksToDraw = openAudUsd[tick-windowToCheck : tick+afterLag+1]
		UsdZarTicksToDraw = openUsdZar[tick-windowToCheck : tick+afterLag+1]
		NzdUsdTicksToDraw = openNzdUsd[tick-windowToCheck : tick+afterLag+1]
		EurNzdTicksToDraw = openEurNzd[tick-windowToCheck : tick+afterLag+1]

		drawAudUsdPlot(tick, AudUsdTicksToDraw, AudUsdData)
		drawNzdUsdPlot(tick, NzdUsdTicksToDraw, NzdUsdData)
		
		drawUsdZarPlot(tick, UsdZarTicksToDraw, UsdZarData)
		drawEurNzdPlot(tick, EurNzdTicksToDraw, EurNzdData)