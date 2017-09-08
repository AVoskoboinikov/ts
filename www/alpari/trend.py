import pandas as pd
import matplotlib.pyplot as plt

def trendSMA(ticks):
	window = 10
	trend = []

	for i in range(1, len(ticks) + 1):
		if i < window:
			series = ticks[0:i]
		else:
			series = ticks[(i-window):i]

		trend.append(sum(series)/len(series))

	return trend

def trendWMA(ticks):
	trend = []

	for i in range(1, len(ticks) + 1):
		series = ticks[0:i]
		trend.append(sum(series)/len(series))

	weights = [(1 + i/len(trend)/5000) for i in range(1, len(trend) + 1)]
	weightedTrend = [a*b for a,b in zip(trend,weights)]

	return weightedTrend

def trendEMA(ticks):
	window = 10
	trend = []
	emaPrev = sum(ticks[0:window])/window

	coef = 2 / (window + 1)

	for i in range(0, len(ticks)):
		ema = (ticks[i] - emaPrev) * coef + emaPrev
		emaPrev = ema
		trend.append(ema)

	return trend

audusdFile = 'NZDUSD1M - last year.csv'
audusd = pd.read_csv(audusdFile, usecols=['Date', 'Time', 'Open'])
openAudUsd = audusd['Open'].values

iterationStep = 100
window = 100

for i in range(0, len(openAudUsd), iterationStep):
	ticks = openAudUsd[i : (i + window + 50)]
	trendTicks = openAudUsd[i : (i + window)]
	
	y_axis = [float(tick) for tick in ticks]
	x_axis = [i for i in range(1, len(y_axis) + 1)]

	trendSMA_values = trendSMA(trendTicks)
	trendSMA_axis = [i for i in range(1, len(trendSMA_values) + 1)]

	trendEMA_values = trendEMA(trendTicks)
	trendEMA_axis = [i for i in range(1, len(trendEMA_values) + 1)]

	plt.plot(x_axis, y_axis, 'g-')
	plt.plot(trendSMA_axis, trendSMA_values, 'r-')
	plt.plot(trendEMA_axis, trendEMA_values, 'b-')
	
	plt.show()
	plt.clf()