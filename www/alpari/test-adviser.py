# if isOK:
	# 	isOK = False

	# 	howManyUseForIndex = 150
	# 	pircedIndex = getTrendGraphPierceIndex(emaTotalTrend[-howManyUseForIndex:], totalPrevTicks[-howManyUseForIndex:])

	# 	if pircedIndex > 0:
	# 		isOK = True


	# if isOK and totalTrendDown:
	# 	howManyUseForIndex = round(len(emaTotalTrend)/2)
	# 	pircedIndex = getTrendGraphPierceIndex(emaTotalTrend[-howManyUseForIndex:], totalPrevTicks[-howManyUseForIndex:])
	# 	pircedIndexTreshold = 0.002

	# 	# if first point of emaTotalTrend < lastPoitn of emaTrend => left OK
	# 	# if first point of emaTotalTrend > lastPoitn of emaTrend => Not OK
	# 	# if first point of emaTotalTrend > lastPoitn of emaTrend and end of the emaTotalTrend is pierced by graph enough => left OK

	# 	isOK = False

	# 	if emaTotalTrend[0] < emaTrend[-1]:
	# 		isOK = True

	# 	if emaTotalTrend[0] > emaTrend[-1] and pircedIndex > pircedIndexTreshold:
	# 		isOK = True

	# if isOK:
	# 	piercedIndexPeriod = 100
	# 	pircedIndex = getTrendGraphPierceWeightedIndex(emaTotalTrend[-piercedIndexPeriod:], totalPrevTicks[-piercedIndexPeriod:])

	# 	diff = max(emaTotalTrend) - max(emaTrend)
	# 	if diff > 0 and pircedIndex == 0:
	# 		isOK = False

	# maybe should be applied
	# diff = abs(max(emaTotalTrend) - max(emaTrend))
	#	if diff > 0.0005 and pircedIndex > 0:
	#		isOK = True

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