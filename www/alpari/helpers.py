
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