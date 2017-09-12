import csv
import pandas as pd
import matplotlib.pyplot as plt

from find_unicorns import findUnicorns
from get_unicorn_index import getUnicornIndex
from trend import trendEMA, isTrendMovingUp, isTrendMovingDown
from volatility import getVolatility, getUpVolatility, getDownVolatility

def drawPlot(index, showLag, checkedWindow, ticks, additionalData):
	y_axis = [float(tick) for tick in ticks]
	x_axis = [i for i in range(1, len(y_axis) + 1)]

	fig = plt.figure()
	fig.set_size_inches(15,8)

	plt.plot(x_axis, y_axis, 'g-')
	plt.axvline(showLag+checkedWindow)

	plotFileName = str(index) + '.png'

	# additionalData['trend']
	trendY_axis = [float(tick) for tick in additionalData['trend']]
	trendX_axis = [i for i in range(showLag+1, len(additionalData['trend']) + showLag+1)]
	plt.plot(trendX_axis, trendY_axis, 'r-')

	# additionalData['totalTrend']
	trendY_axis = [float(tick) for tick in additionalData['totalTrend']]
	trendX_axis = [i for i in range(100, len(additionalData['totalTrend']) + 100)]
	plt.plot(trendX_axis, trendY_axis, 'b-')

	# additionalData['volatility'] and additionalData['maxVolatility']
	plt.figtext(0.05, 0.95, "V: " + str(format(additionalData['volatility'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.05, 0.9, "Max V: " + str(format(additionalData['maxVolatility'], 'f')), color="black", weight=500, size="medium")

	# additionalData['upVolatility'] and additionalData['maxUpVolatility']
	plt.figtext(0.2, 0.95, "Vup: " + str(format(additionalData['upVolatility'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.2, 0.9, "Max Vup: " + str(format(additionalData['maxUpVolatility'], 'f')), color="black", weight=500, size="medium")

	# additionalData['downVolatility'] and additionalData['maxDownVolatility']
	plt.figtext(0.35, 0.95, "Vdn: " + str(format(additionalData['downVolatility'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.35, 0.9, "Max Vdn: " + str(format(additionalData['maxDownVolatility'], 'f')), color="black", weight=500, size="medium")

	# additionalData['upVolatility']/additionalData['downVolatility'] and additionalData['maxUpVolatility']/additionalData['maxDownVolatility']
	plt.figtext(0.5, 0.95, "Vup/Vdn: " + str(format(additionalData['upVolatility']/additionalData['downVolatility'], 'f')), color="black", weight=500, size="medium")
	plt.figtext(0.5, 0.9, "Max Vup/Max Vdn: " + str(format(additionalData['maxUpVolatility']/additionalData['maxDownVolatility'], 'f')), color="black", weight=500, size="medium")

	# additionalData['totalUp'] and additionalData['totalDown']
	plt.figtext(0.65, 0.95, "Total Up: " + str(additionalData['totalUp']), color="black", weight=500, size="medium")
	plt.figtext(0.65, 0.9, "Total Down: " + str(additionalData['totalDown']), color="black", weight=500, size="medium")		

	# additionalData['totalUp']/additionalData['totalDown']
	plt.figtext(0.8, 0.95, "Total Up / Total Down: " + str(format(additionalData['totalUp']/additionalData['totalDown'], 'f')), color="black", weight=500, size="medium")

	# plt.show()

	plt.savefig('../plots/positive/' + plotFileName)

	plt.clf()
	plt.close(fig)

# fileToRead = 'AUDUSD1M - last year.csv'
# fileToRead = 'AUDUSD1M.csv'
fileToRead = 'NZDUSD1M - last year.csv'
# fileToRead = 'NZDUSD1M.csv'

audusd = pd.read_csv(fileToRead, usecols=['Date', 'Time', 'Open'])
openAudUsd = audusd['Open'].values

del audusd

windowToCheck = 75
showLag = 50
ticksStep = 10

beforeLag = 8*showLag
afterLag = 4*showLag


for tick in range(windowToCheck + beforeLag, len(openAudUsd), ticksStep):
	
	sampleTicks = openAudUsd[tick-windowToCheck : tick]
	totalPrevTicks = openAudUsd[tick-windowToCheck-6*showLag : tick-windowToCheck]

	isOK = False

	emaTrend = trendEMA(sampleTicks, 5, 2)
	trendUp = isTrendMovingUp(emaTrend, 10)

	emaTotalTrend = trendEMA(totalPrevTicks, 15, 0.1) # 25, 0.2
	totalTrendDown = isTrendMovingDown(emaTotalTrend, 25) # 35

	sampleVolatility, sampleMaxVolatility = getVolatility(sampleTicks)
	sampleUpVolatility, sampleUpMaxVolatility = getUpVolatility(sampleTicks)
	sampleDownVolatility, sampleDownMaxVolatility = getDownVolatility(sampleTicks)

	totalUp, totalDown = getUnicornIndex(sampleTicks)
	totalUp = round(totalUp, 4)
	totalDown = round(totalDown, 4)

	if trendUp and totalTrendDown:
		isOK = True

	# conditions
	# if first point of emaTotalTrend < lastPoitn of emaTrend => left OK
	# if first point of emaTotalTrend > lastPoitn of emaTrend => Not OK
	# if first point of emaTotalTrend > lastPoitn of emaTrend and end of the emaTotalTrend is pierced by graph enough => left OK

	# maybe should be applied # magick numbers
	# if sampleMaxVolatility > 0.001:
	# 	isOK = False

	# maybe should be applied # magick numbers
	# if sampleMaxVolatility >= 0.0008:
	# 	isOK = False	

	# maybe should be applied # magick numbers
	# if totalUp >= 0.005:
		# isOK = False

	# maybe should be applied # magick numbers
	# if sampleUpVolatility/sampleDownVolatility > 1.8:
	# 	isOK = False

	# maybe should be applied # magick numbers
	# if sampleMaxVolatility/sampleDownMaxVolatility > 2 and sampleUpVolatility/sampleDownVolatility < 1.2 and totalUp/totalDown >= 2:
	# 	isOK = False

	# maybe should be applied # magick numbers
	# if totalUp/totalDown >= 2.3 and totalUp >= 0.003:
	# 	isOK = False

	if isOK:
		ticksToDraw = openAudUsd[tick-windowToCheck-beforeLag : tick+afterLag]
		dataToPass = {
			'trend': emaTrend,
			'totalTrend': emaTotalTrend,
			'volatility': sampleVolatility,
			'maxVolatility': sampleMaxVolatility,
			'upVolatility': sampleUpVolatility,
			'maxUpVolatility': sampleUpMaxVolatility,
			'downVolatility': sampleDownVolatility,
			'maxDownVolatility': sampleDownMaxVolatility,
			'totalUp': totalUp,
			'totalDown': totalDown,
		}
		drawPlot(tick, beforeLag, windowToCheck, ticksToDraw, dataToPass)