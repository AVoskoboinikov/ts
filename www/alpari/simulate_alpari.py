import pandas as pd
import matplotlib.pyplot as plt
import time
import random

from advisers import adviserThreeSteps
from advisers import adviserTrendUp
from advisers import alwaysTrue
from advisers import alwaysFalse

def drawPlot(index, nzdHisoryTicks, audHisoryTicks, openTick, closeTick, isPositive):
	audNzdCoef = (audHisoryTicks[0] - nzdHisoryTicks[0])%0.001
	if audNzdCoef > 0.005:
		audNzdCoef -= 0.005
	audNzdDiff = audHisoryTicks[0] - nzdHisoryTicks[0] - audNzdCoef

	nzd_y_axis = [float(tick) for tick in nzdHisoryTicks]
	aud_y_axis = [float(tick)-audNzdDiff for tick in audHisoryTicks]
	x_axis = [i for i in range(1, len(nzd_y_axis) + 1)]

	fig = plt.figure()
	fig.set_size_inches(15,8)
	plt.grid()

	plt.plot(x_axis, nzd_y_axis, 'g-')
	plt.plot(x_axis, aud_y_axis, 'm-')
	plt.axvline(openTick)
	plt.axvline(closeTick)

	plotFileName = str(index) + '.png'

	if isPositive == True:
		path = '../plots/positive/'

	if isPositive == False:
		path = '../plots/negative/'

	# plt.show()
	plt.savefig(path + plotFileName)

	plt.clf()
	plt.close(fig)






fileToReadAUD = 'AUDUSD1M - last year.csv'
# audusdFile = 'AUDUSD1M.csv'
fileToReadNZD = 'NZDUSD1M - last year.csv'
# audusdFile = 'NZDUSD1M.csv'

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

isOrderPlaced = False
orderPlaceValue = 0
orderPlaceTick = 0
totalProfit = 0
totalLoss = 0
stopLossCountFromTick = 0
window = 450
stopLoss = 0.0007
# stopProfit = 0.0009
totalLossBiggerThanTotalProfit = 0

for tick in range(window, len(openNzdUsd)):
	if isOrderPlaced == False:
		history = openNzdUsd[(tick-window) : (tick+1)]

		if adviserTrendUp(history):
			isOrderPlaced = True
			orderPlaceValue = openNzdUsd[tick]
			orderPlaceTick = tick
			stopLossCountFromTick = tick

	if isOrderPlaced == True:
		tickDiff = openNzdUsd[tick] - openNzdUsd[stopLossCountFromTick]

		if tickDiff < 0 and abs(tickDiff) >= stopLoss:
			win = False
			isOrderPlaced = False
			totalDiff = openNzdUsd[tick] - openNzdUsd[orderPlaceTick]

			if totalDiff > 0:
				win = True
				totalProfit += abs(totalDiff)

			if totalDiff < 0:
				totalLoss += abs(totalDiff)

			if totalLoss > totalProfit:
				totalLossBiggerThanTotalProfit += 1

			startFrom = orderPlaceTick-window
			orderOpenTick = window
			nzdHistoryToDraw = openNzdUsd[startFrom : tick+50]
			audHistoryToDraw = openAudUsd[startFrom : tick+50]
			orderCloseTick = len(nzdHistoryToDraw) - 50

			drawPlot(orderPlaceTick, nzdHistoryToDraw, audHistoryToDraw, orderOpenTick, orderCloseTick, win)

		if tickDiff > 0:
			stopLossCountFromTick = tick
			
			# isOrderPlaced = False
			# totalProfit += abs(tickDiff)
			# drawPlot(tick, (tick - orderPlaceTick), openAudUsd[(orderPlaceTick-2*window) : (tick + 1)], True)

print('Total profit:', totalProfit)
print('Total loss:', totalLoss)
print('Profit:', totalProfit - totalLoss)
print('Bellow zero:', totalLossBiggerThanTotalProfit)