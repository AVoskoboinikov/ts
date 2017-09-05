import pandas as pd
from advicers import advicerThreeSteps
from advicers import alwaysTrue
from advicers import alwaysFalse

audusdFile = 'AUDUSD1M - last year.csv'
audusd = pd.read_csv(audusdFile, usecols=['Date', 'Time', 'Open'])
openAudUsd = audusd['Open'].values

isOrderPlaced = False
orderPlaceValue = 0
totalProfit = 0
totalLoss = 0
window = 50
stopLoss = 0.0007
stopProfit = 0.001

for tick in range(window, len(openAudUsd)):

	if isOrderPlaced == False:
		history = openAudUsd[(tick-window) : tick]

		if advicerThreeSteps(history) == True:
			isOrderPlaced = True
			orderPlaceValue = openAudUsd[tick]

	if isOrderPlaced == True:
		tickDiff = openAudUsd[tick] - orderPlaceValue

		if tickDiff < 0 and abs(tickDiff) >= stopLoss:
			isOrderPlaced = False
			totalLoss += abs(tickDiff)

		if tickDiff > 0 and abs(tickDiff) >= stopProfit:
			isOrderPlaced = False
			totalProfit += abs(tickDiff)

print('Total profit:', totalProfit)
print('Total loss:', totalLoss)
print('Profit:', totalProfit - totalLoss)