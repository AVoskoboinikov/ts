
def getTrendGraphPierceIndex(trendTicks, graphTicks):
	index = 0

	for i in range(0, len(trendTicks)):
		if graphTicks[i] > trendTicks[i]:
			index += abs(graphTicks[i] - trendTicks[i])

	return index

def getTrendGraphPierceWeightedIndex(trendTicks, graphTicks):
	index = 0
	initialWeight = 1

	for i in range(0, len(trendTicks)):
		weight = initialWeight + i * 2

		if graphTicks[i] > trendTicks[i]:
			index += weight * abs(graphTicks[i] - trendTicks[i])

	return index

def getTrendGraphUnPierceWeightedIndex(trendTicks, graphTicks):
	index = 0
	initialWeight = 1

	for i in range(0, len(trendTicks)):
		weight = initialWeight + i * 2

		if graphTicks[i] < trendTicks[i]:
			index += weight * abs(graphTicks[i] - trendTicks[i])

	return index

def linesNotCross(line1, line2):
	for i in range(len(line1)):
		x1 = line1[i]
		x2 = line2[i]

		if x1 < x2 and abs(x2 - x1) >= 0.00005:
			return False

	return True
