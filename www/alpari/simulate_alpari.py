import pandas as pd
import matplotlib.pyplot as plt
from advisers import adviserThreeSteps
from advisers import alwaysTrue
from advisers import alwaysFalse

# audusdFile = 'AUDUSD1M - last year.csv'
# audusdFile = 'AUDUSD1M.csv'
# audusdFile = 'NZDUSD1M - last year.csv'
audusdFile = 'NZDUSD1M.csv'

def drawPlot(index, orderTick, ticks, isPositive):
	y_axis = [float(tick) for tick in ticks]
	x_axis = [i for i in range(1, len(y_axis) + 1)]

	plt.plot(x_axis, y_axis, 'g-')
	plt.axvline(len(ticks) - orderTick)

	plotFileName = str(index) + '.png'

	if isPositive == True:
		plt.savefig('../plots/positive/' + plotFileName)

	if isPositive == False:
		plt.savefig('../plots/negative/' + plotFileName)

	plt.clf()


audusd = pd.read_csv(audusdFile, usecols=['Date', 'Time', 'Open'])
openAudUsd = audusd['Open'].values

isOrderPlaced = False
orderPlaceValue = 0
orderPlaceTick = 0
totalProfit = 0
totalLoss = 0
window = 50
stopLoss = 0.0007
stopProfit = 0.0009
totalLossBiggerThanTotalProfit = 0

for tick in range(window, len(openAudUsd)):
	if isOrderPlaced == False:
		history = openAudUsd[(tick-window) : tick]

		if adviserThreeSteps(history) == True:
			isOrderPlaced = True
			orderPlaceValue = openAudUsd[tick]
			orderPlaceTick = tick

	if isOrderPlaced == True:
		tickDiff = openAudUsd[tick] - orderPlaceValue

		if tickDiff < 0 and abs(tickDiff) >= stopLoss:
			isOrderPlaced = False
			totalLoss += abs(tickDiff)

			if totalLoss > totalProfit:
				totalLossBiggerThanTotalProfit += 1

			# drawPlot(tick, (tick - orderPlaceTick), openAudUsd[(orderPlaceTick-window) : tick], False)

		if tickDiff > 0 and abs(tickDiff) >= stopProfit:
			isOrderPlaced = False
			totalProfit += abs(tickDiff)
			# drawPlot(tick, (tick - orderPlaceTick), openAudUsd[(orderPlaceTick-window) : tick], True)

print('Total profit:', totalProfit)
print('Total loss:', totalLoss)
print('Profit:', totalProfit - totalLoss)
print('Bellow zero:', totalLossBiggerThanTotalProfit)