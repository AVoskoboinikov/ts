import pandas as pd

def trendEMA(ticks, window, magickCoef):
	trend = []
	emaPrev = sum(ticks[0:window])/window

	coef = magickCoef / (window + 1)

	for i in range(0, len(ticks)):
		ema = (ticks[i] - emaPrev) * coef + emaPrev
		emaPrev = ema
		trend.append(ema)

	return trend

def isTrendMovingUp(ticks, window):
	series = []

	for i in range(0, len(ticks), window):
		subSeries = ticks[i:i+window]
		
		# if len(subSeries) == window:
		series.append(sum(subSeries)/len(subSeries))

	series.append(ticks[-1])

	return series == sorted(series)

def isTrendMovingDown(ticks, window):
	series = []

	for i in range(0, len(ticks), window):
		subSeries = ticks[i:i+window]
		
		# if len(subSeries) == window:
		series.append(sum(subSeries)/len(subSeries))

	series.append(ticks[-1])

	return series == sorted(series, reverse=True)

def isTrendMovingUp2(ticks):
	sumUp = 0
	sumDown = 0

	for i in range(1, len(ticks)):
		diff = ticks[i] - ticks[i-1]
		
		if diff > 0:
			sumUp += diff

		if diff < 0:
			sumDown += abs(diff)

	return sumUp > sumDown

def isTrendMovingDown2(ticks):
	sumUp = 0
	sumDown = 0

	for i in range(1, len(ticks)):
		diff = ticks[i] - ticks[i-1]
		
		if diff > 0:
			sumUp += diff

		if diff < 0:
			sumDown += abs(diff)

	return sumDown > sumUp

def getCorr(corrFrom, corrTo):
	corr = 0

	df = pd.DataFrame.from_items([('corrFrom', corrFrom), ('corrTo', corrTo)])
	corr = df.corr()

	return corr['corrFrom']['corrTo']

def getUnicornIndex(breadCrumbs):
	upIndex = 0
	downIndex = 0

	for i in range(1, len(breadCrumbs)):
		x1 = breadCrumbs[i-1]
		x2 = breadCrumbs[i]
		diff = x2 - x1

		if diff > 0:
			upIndex += diff

		if diff < 0:
			downIndex += (-1) * diff

	return upIndex, downIndex