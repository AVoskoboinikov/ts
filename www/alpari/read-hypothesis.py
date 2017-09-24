import csv
import pandas as pd
import matplotlib.pyplot as plt
import math

from find_unicorns import findUnicorns
from get_unicorn_index import getUnicornIndex
from trend import trendEMA, isTrendMovingUp, isTrendMovingDown
from volatility import getVolatility, getUpVolatility, getDownVolatility
from helpers import getTrendGraphPierceIndex, getTrendGraphPierceWeightedIndex, getTrendGraphUnPierceWeightedIndex

from advisers import adviserTrendUp

def drawPlot(index, showLag, checkedWindow, nzdTicksToDraw, audTicksToDraw, additionalData):
	# audNzdDiff = math.floor((audTicksToDraw[0] - nzdTicksToDraw[0])*100)/100
	# audNzdDiff = round(audTicksToDraw[0] - nzdTicksToDraw[0], 2)
	audNzdCoef = (audTicksToDraw[0] - nzdTicksToDraw[0])%0.001
	if audNzdCoef > 0.005:
		audNzdCoef -= 0.005
	audNzdDiff = audTicksToDraw[0] - nzdTicksToDraw[0] - audNzdCoef
	
	nzd_y_axis = [float(tick) for tick in nzdTicksToDraw]
	aud_y_axis = [float(tick)-audNzdDiff for tick in audTicksToDraw]
	x_axis = [i for i in range(1, len(nzd_y_axis) + 1)]

	fig = plt.figure()
	fig.set_size_inches(15,8)

	plt.plot(x_axis, nzd_y_axis, 'g-')
	plt.plot(x_axis, aud_y_axis, 'm-')
	plt.axvline(showLag+checkedWindow)

	plotFileName = str(index) + '.png'

	# additionalData['nanoTrend']
	nanoTrendLength = len(additionalData['nanoTrend1'])
	trendY_axis = [float(tick) for tick in additionalData['nanoTrend1']]
	trendX_axis = [i for i in range(showLag+checkedWindow-nanoTrendLength+1, len(additionalData['nanoTrend1']) + showLag+checkedWindow-nanoTrendLength+1)]
	plt.plot(trendX_axis, trendY_axis, 'm-')

	# additionalData['nanoTrend']
	nanoTrendLength = len(additionalData['nanoTrend2'])
	trendY_axis = [float(tick) for tick in additionalData['nanoTrend2']]
	trendX_axis = [i for i in range(showLag+checkedWindow-nanoTrendLength+1, len(additionalData['nanoTrend2']) + showLag+checkedWindow-nanoTrendLength+1)]
	plt.plot(trendX_axis, trendY_axis, 'c-')

	# additionalData['nanoTrend']
	nanoTrendLength = len(additionalData['nanoTrend3'])
	trendY_axis = [float(tick) for tick in additionalData['nanoTrend3']]
	trendX_axis = [i for i in range(showLag+checkedWindow-nanoTrendLength+1, len(additionalData['nanoTrend3']) + showLag+checkedWindow-nanoTrendLength+1)]
	plt.plot(trendX_axis, trendY_axis, 'k-')

	# additionalData['subTrend']
	subTrendLength = len(additionalData['subTrend'])
	trendY_axis = [float(tick) for tick in additionalData['subTrend']]
	trendX_axis = [i for i in range(showLag+checkedWindow-subTrendLength+1, len(additionalData['subTrend']) + showLag+checkedWindow-subTrendLength+1)]
	plt.plot(trendX_axis, trendY_axis, 'y-')

	# additionalData['trend']
	trendY_axis = [float(tick) for tick in additionalData['trend']]
	trendX_axis = [i for i in range(showLag+1, len(additionalData['trend']) + showLag+1)]
	plt.plot(trendX_axis, trendY_axis, 'r-')

	# additionalData['totalTrend']
	# trendY_axis = [float(tick) for tick in additionalData['totalTrend']]
	# trendX_axis = [i for i in range(0, len(additionalData['totalTrend']))]
	# plt.plot(trendX_axis, trendY_axis, 'b-')

	# trend distance
	plt.figtext(0.05, 0.975, "Summ: " + str(format(additionalData['trendDistance1'] + additionalData['trendDistance2'] + additionalData['trendDistance3'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.05, 0.95, "Distance1: " + str(format(additionalData['trendDistance1'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.05, 0.925, "Distance2: " + str(format(additionalData['trendDistance2'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.05, 0.9, "Distance3: " + str(format(additionalData['trendDistance3'], 'f')), color="black", weight=500, size="medium")

	plt.figtext(0.175, 0.95, "Up1: " + str(int(additionalData['trendUp1'])), color="black", weight=500, size="medium")
	plt.figtext(0.175, 0.925, "Up2: " + str(int(additionalData['trendUp2'])), color="black", weight=500, size="medium")
	plt.figtext(0.175, 0.9, "Up3: " + str(int(additionalData['trendUp3'])), color="black", weight=500, size="medium")

	plt.figtext(0.225, 0.95, "Down1: " + str(int(additionalData['trendDown1'])), color="black", weight=500, size="medium")
	plt.figtext(0.225, 0.925, "Down2: " + str(int(additionalData['trendDown2'])), color="black", weight=500, size="medium")
	plt.figtext(0.225, 0.9, "Down3: " + str(int(additionalData['trendDown3'])), color="black", weight=500, size="medium")

	plt.figtext(0.3, 0.975, "Trend 1 Diff: " + str(format(additionalData['emaTrendDiff'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.3, 0.95, "Trend 2 Diff: " + str(format(additionalData['emaSubTrendDiff'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.3, 0.925, "Trend 3 Diff: " + str(format(additionalData['emaNanoTrend1Diff'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.3, 0.9, "Trend 4 Diff: " + str(format(additionalData['emaNanoTrend2Diff'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.3, 0.875, "Trend 5 Diff: " + str(format(additionalData['emaNanoTrend3Diff'], 'f')), color="black", weight=500, size="medium")

	plt.figtext(0.45, 0.975, "Trend 2/1: " + str(format(additionalData['emaSubTrendDiff']/additionalData['emaTrendDiff'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.45, 0.95, "Trend 3/2: " + str(format(additionalData['emaNanoTrend1Diff']/additionalData['emaSubTrendDiff'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.45, 0.925, "Trend 4/3: " + str(format(additionalData['emaNanoTrend2Diff']/additionalData['emaNanoTrend1Diff'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.45, 0.9, "Trend 5/4: " + str(format(additionalData['emaNanoTrend3Diff']/additionalData['emaNanoTrend2Diff'], 'f')), color="black", weight=500, size="medium")

	plt.figtext(0.65, 0.975, "Trend 2-1: " + str(format(additionalData['emaSubTrendDiff']-additionalData['emaTrendDiff'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.65, 0.95, "Trend 3-2: " + str(format(additionalData['emaNanoTrend1Diff']-additionalData['emaSubTrendDiff'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.65, 0.925, "Trend 4-3: " + str(format(additionalData['emaNanoTrend2Diff']-additionalData['emaNanoTrend1Diff'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.65, 0.9, "Trend 5-4: " + str(format(additionalData['emaNanoTrend3Diff']-additionalData['emaNanoTrend2Diff'], 'f')), color="black", weight=500, size="medium")

	# # additionalData['volatility'] and additionalData['maxVolatility']
	# plt.figtext(0.05, 0.95, "V: " + str(format(additionalData['volatility'], 'f')), color="black", weight=500, size="medium")
	# plt.figtext(0.05, 0.9, "Max V: " + str(format(additionalData['maxVolatility'], 'f')), color="black", weight=500, size="medium")

	# # additionalData['upVolatility'] and additionalData['maxUpVolatility']
	# plt.figtext(0.2, 0.95, "Vup: " + str(format(additionalData['upVolatility'], 'f')), color="black", weight=500, size="medium")
	# plt.figtext(0.2, 0.9, "Max Vup: " + str(format(additionalData['maxUpVolatility'], 'f')), color="black", weight=500, size="medium")

	# # additionalData['downVolatility'] and additionalData['maxDownVolatility']
	# plt.figtext(0.35, 0.95, "Vdn: " + str(format(additionalData['downVolatility'], 'f')), color="black", weight=500, size="medium")
	# plt.figtext(0.35, 0.9, "Max Vdn: " + str(format(additionalData['maxDownVolatility'], 'f')), color="black", weight=500, size="medium")

	# # additionalData['upVolatility']/additionalData['downVolatility'] and additionalData['maxUpVolatility']/additionalData['maxDownVolatility']
	# plt.figtext(0.5, 0.95, "Vup/Vdn: " + str(format(additionalData['upVolatility']/additionalData['downVolatility'], 'f')), color="black", weight=500, size="medium")
	# plt.figtext(0.5, 0.9, "Max Vup/Max Vdn: " + str(format(additionalData['maxUpVolatility']/additionalData['maxDownVolatility'], 'f')), color="black", weight=500, size="medium")

	# # additionalData['totalUp'] and additionalData['totalDown']
	# plt.figtext(0.65, 0.95, "Total Up: " + str(additionalData['totalUp']), color="black", weight=500, size="medium")
	# plt.figtext(0.65, 0.9, "Total Down: " + str(additionalData['totalDown']), color="black", weight=500, size="medium")		

	# # additionalData['totalUp']/additionalData['totalDown']
	# plt.figtext(0.8, 0.95, "Pierced: " + str(format(additionalData['pircedIndex'], 'f')), color="black", weight=500, size="medium")
	# plt.figtext(0.8, 0.925, "Un pierced: " + str(format(additionalData['unPircedIndex'], 'f')), color="black", weight=500, size="medium")
	# plt.figtext(0.8, 0.90, "Pierced/Un pierced: " + str(format(additionalData['pircedIndex']/additionalData['unPircedIndex'], 'f')), color="black", weight=500, size="medium")

	plt.grid()

	# plt.show()
	plt.savefig('../plots/hypothesis/' + plotFileName)

	plt.clf()
	plt.close(fig)

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

openAudUsd = audnzd['Open AUDUSD'].values
openNzdUsd = audnzd['Open NZDUSD'].values

del audusd
del nzdusd
del audnzd

windowToCheck = 150
showLag = 50
ticksStep = 1

beforeLag = 8*showLag
afterLag = 4*showLag

skipTicks = 0

for tick in range(windowToCheck + 6*showLag, len(openNzdUsd), ticksStep):
	
	if skipTicks > 0:
		skipTicks -= 1
		continue

	sampleTicks = openNzdUsd[tick-windowToCheck-6*showLag+1 : tick+1]
	isOK = adviserTrendUp(sampleTicks)

	if isOK:
		skipTicks = 30

		nanoTrendTicks1 = sampleTicks[-45 : ]
		nanoTrendTicks2 = sampleTicks[-35 : ]
		nanoTrendTicks3 = sampleTicks[-25 : ]
		
		subTrendTicks = sampleTicks[-75 : ]
		trendTicks = sampleTicks[-150 : ]
		totalTrendTicks = sampleTicks[-450 : -150]

		emaNanoTrend1 = trendEMA(nanoTrendTicks1, 4, 0.4)
		emaNanoTrend1Up = isTrendMovingUp(emaNanoTrend1, 5)
		emaNanoTrend1Down = isTrendMovingDown(emaNanoTrend1, 5)
		# emaNanoTrend1Diff = max(nanoTrendTicks1[-3:]) - min(nanoTrendTicks1[:3])
		emaNanoTrend1UpDiff, emaNanoTrend1DownDiff = getUnicornIndex(nanoTrendTicks1)
		emaNanoTrend1Diff = emaNanoTrend1UpDiff - emaNanoTrend1DownDiff
		emaNanoTrend1Diff += 0.000001
		
		emaNanoTrend2 = trendEMA(nanoTrendTicks2, 4, 0.4)
		emaNanoTrend2Up = isTrendMovingUp(emaNanoTrend2, 5)
		emaNanoTrend2Down = isTrendMovingDown(emaNanoTrend2, 5)
		# emaNanoTrend2Diff = max(nanoTrendTicks2[-3:]) - min(nanoTrendTicks2[:3])
		emaNanoTrend2UpDiff, emaNanoTrend2DownDiff = getUnicornIndex(nanoTrendTicks2)
		emaNanoTrend2Diff = emaNanoTrend2UpDiff - emaNanoTrend2DownDiff
		emaNanoTrend2Diff += 0.000001
		
		emaNanoTrend3 = trendEMA(nanoTrendTicks3, 4, 0.4)
		emaNanoTrend3Up = isTrendMovingUp(emaNanoTrend3, 5)
		emaNanoTrend3Down = isTrendMovingDown(emaNanoTrend3, 5)
		# emaNanoTrend3Diff = max(nanoTrendTicks3[-3:]) - min(nanoTrendTicks3[:3])
		emaNanoTrend3UpDiff, emaNanoTrend3DownDiff = getUnicornIndex(nanoTrendTicks3)
		emaNanoTrend3Diff = emaNanoTrend3UpDiff - emaNanoTrend3DownDiff
		emaNanoTrend3Diff += 0.000001

		emaSubTrend = trendEMA(subTrendTicks, 4, 0.4)
		# emaSubTrendDiff = max(subTrendTicks[-3:]) - min(subTrendTicks[:3])
		emaSubTrendUpDiff, emaSubTrendDownDiff = getUnicornIndex(subTrendTicks)
		emaSubTrendDiff = emaSubTrendUpDiff - emaSubTrendDownDiff
		emaSubTrendDiff += 0.000001

		emaTrend = trendEMA(trendTicks, 5, 0.2)
		# emaTrendDiff = max(trendTicks[-3:]) - min(trendTicks[:3])		
		emaTrendUpDiff, emaTrendDownDiff = getUnicornIndex(trendTicks)
		emaTrendDiff = emaTrendUpDiff - emaTrendDownDiff
		emaTrendDiff += 0.000001

		emaTotalTrend = trendEMA(totalTrendTicks, 25, 0.2)

		trendDistance1 = emaNanoTrend1[0]-emaSubTrend[-len(nanoTrendTicks1)]
		trendDistance2 = emaNanoTrend2[0]-emaSubTrend[-len(nanoTrendTicks2)]
		trendDistance3 = emaNanoTrend3[0]-emaSubTrend[-len(nanoTrendTicks3)]
		# trendDistance = getTrendGraphPierceWeightedIndex(emaSubTrend[-len(emaNanoTrend):], emaNanoTrend)

		# isOK = False

		# if emaNanoTrend1Diff <= 0 or emaNanoTrend2Diff <= 0 or emaNanoTrend3Diff <= 0 or emaSubTrendDiff <= 0 or emaTrendDiff <= 0:
			# isOK = True
	
	# totalPrevTicks = openNzdUsd[tick-windowToCheck-6*showLag : tick-windowToCheck+1]

	# isOK = False

	# emaTrend = trendEMA(sampleTicks, 5, 0.2)
	# trendUp = isTrendMovingUp(emaTrend, 10)

	# emaTotalTrend = trendEMA(totalPrevTicks, 25, 0.2) # 25, 0.2
	# totalTrendDown = isTrendMovingDown(emaTotalTrend, 35) # 35
	# totalTrendUp = isTrendMovingUp(emaTotalTrend, 35)

	# sampleVolatility, sampleMaxVolatility = getVolatility(sampleTicks)
	# sampleUpVolatility, sampleUpMaxVolatility = getUpVolatility(sampleTicks)
	# sampleDownVolatility, sampleDownMaxVolatility = getDownVolatility(sampleTicks)

	# totalUp, totalDown = getUnicornIndex(sampleTicks)
	# totalUp = round(totalUp, 4)
	# totalDown = round(totalDown, 4)

	# piercedUpIndex = getTrendGraphPierceWeightedIndex(emaTotalTrend, totalPrevTicks)
	# piercedDownIndex = getTrendGraphUnPierceWeightedIndex(emaTotalTrend, totalPrevTicks)

	# if trendUp:
	# 	isOK = True

	# if isOK:
	# 	isOK = False

	# 	subTrendWindow = 75
	# 	subTrendTicks = openNzdUsd[tick-subTrendWindow : tick]
	# 	emaSubTrend = trendEMA(subTrendTicks, 4, 0.4)
	# 	subTrendUp = isTrendMovingUp(emaSubTrend, 10)

	# 	if subTrendUp:
	# 		isOK = True

	# if isOK and totalTrendDown:
	# 	isOK = False

	# 	if min(emaTotalTrend) > max(emaTrend):
	# 		isOK = True

	# if isOK:
	# 	isOK = False

	# 	if sampleUpVolatility < 0.00015:
	# 		isOK = True

	
	if isOK:
		nzdTicksToDraw = openNzdUsd[tick-windowToCheck-6*showLag : tick+afterLag+1]
		audTicksToDraw = openAudUsd[tick-windowToCheck-6*showLag : tick+afterLag+1]
		dataToPass = {
			'nanoTrend1': emaNanoTrend1,
			'nanoTrend2': emaNanoTrend2,
			'nanoTrend3': emaNanoTrend3,
			
			'subTrend': emaSubTrend,
			'trend': emaTrend,
			'totalTrend': emaTotalTrend,
			
			'trendDistance1': trendDistance1,
			'trendUp1': emaNanoTrend1Up,
			'trendDown1': emaNanoTrend1Down,
			
			'trendDistance2': trendDistance2,
			'trendUp2': emaNanoTrend2Up,
			'trendDown2': emaNanoTrend2Down,
			
			'trendDistance3': trendDistance3,
			'trendUp3': emaNanoTrend3Up,
			'trendDown3': emaNanoTrend3Down,

			'emaNanoTrend1Diff': emaNanoTrend1Diff,
			'emaNanoTrend2Diff': emaNanoTrend2Diff,
			'emaNanoTrend3Diff': emaNanoTrend3Diff,
			'emaSubTrendDiff': emaSubTrendDiff,
			'emaTrendDiff': emaTrendDiff,
			
			# 'volatility': sampleVolatility,
			# 'maxVolatility': sampleMaxVolatility,
			# 'upVolatility': sampleUpVolatility,
			# 'maxUpVolatility': sampleUpMaxVolatility,
			# 'downVolatility': sampleDownVolatility,
			# 'maxDownVolatility': sampleDownMaxVolatility,
			# 'totalUp': totalUp,
			# 'totalDown': totalDown,
			# 'pircedIndex': piercedUpIndex,
			# 'unPircedIndex': piercedDownIndex
		}
		drawPlot(tick, 6*showLag, windowToCheck, nzdTicksToDraw, audTicksToDraw, dataToPass)