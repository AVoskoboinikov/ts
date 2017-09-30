# import pandas as pd
# import matplotlib.pyplot as plt

def getVolatility(ticks, period):
	volatilitySeries = []

	for i in range(period, len(ticks)):
		volatilitySeries.append(abs(ticks[i] - ticks[i-period]))

	volatilitySeries = sorted(volatilitySeries)

	maxVolatility = volatilitySeries[-1]
	
	shortedSeries = volatilitySeries[:-1]
	volatility = sum(shortedSeries)/len(shortedSeries)

	return volatility, maxVolatility, volatilitySeries

def getUpVolatility(ticks):
	volatilitySeries = []

	for i in range(1, len(ticks)):
		diff = ticks[i] - ticks[i-1]

		if diff > 0:
			volatilitySeries.append(abs(diff))

	volatilitySeries = sorted(volatilitySeries)
	shortedSeries = volatilitySeries[5:]

	volatility = sum(shortedSeries)/len(shortedSeries)
	maxVolatility = max(shortedSeries)

	return volatility, maxVolatility

def getDownVolatility(ticks):
	volatilitySeries = []

	for i in range(1, len(ticks)):
		diff = ticks[i] - ticks[i-1]

		if diff < 0:
			volatilitySeries.append(abs(diff))

	volatilitySeries = sorted(volatilitySeries)
	shortedSeries = volatilitySeries[5:]

	volatility = sum(shortedSeries)/len(shortedSeries)
	maxVolatility = max(shortedSeries)

	return volatility, maxVolatility

# audusdFile = 'NZDUSD1M - last year.csv'
# audusd = pd.read_csv(audusdFile, usecols=['Date', 'Time', 'Open'])
# openAudUsd = audusd['Open'].values

# iterationStep = 100
# window = 100

# for i in range(0, len(openAudUsd), iterationStep):
# 	ticks = openAudUsd[i : (i + window)]
# 	volatility, maxVolatility = getVolatility(ticks)
	
# 	volatility = round(volatility, 6)
# 	maxVolatility = round(maxVolatility, 6)
	
# 	y_axis = [float(tick) for tick in ticks]
# 	x_axis = [i for i in range(1, len(y_axis) + 1)]

# 	plt.plot(x_axis, y_axis, 'g-')
# 	plt.figtext(0.05, 0.95, "Volatility1: " + str(format(volatility, 'f')), color="black", weight=500, size="medium")
# 	plt.figtext(0.05, 0.9, "Volatility2: " + str(format(maxVolatility, 'f')), color="black", weight=500, size="medium")
	
# 	plt.show()
# 	plt.clf()