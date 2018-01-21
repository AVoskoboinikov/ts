from helpers import getCorr, trendEMA, isTrendMovingUp2, isTrendMovingDown2, getUnicornIndex

def adviserCorrelation(audUsdTicks, usdZarTicks, nzdUsdTicks, eurNzdTicks):
	AudUsdNzdUsdCorr = getCorr(audUsdTicks[-15:], nzdUsdTicks[-15:])
	AudUsdUsdZarCorr = getCorr(audUsdTicks[-15:], usdZarTicks[-15:])
	NzdUsdEurNzdCorr = getCorr(nzdUsdTicks[-15:], eurNzdTicks[-15:])

	AudUsdNzdUsdCorrPrev = getCorr(audUsdTicks[:-15], nzdUsdTicks[:-15])

	prevCorrs = []
	prevCorrs.append(getCorr(audUsdTicks[:5], nzdUsdTicks[:5]))
	prevCorrs.append(getCorr(audUsdTicks[5:10], nzdUsdTicks[5:10]))
	prevCorrs.append(getCorr(audUsdTicks[10:15], nzdUsdTicks[10:15]))

	newCorrs = []
	newCorrs.append(getCorr(audUsdTicks[15:20], nzdUsdTicks[15:20]))
	newCorrs.append(getCorr(audUsdTicks[20:25], nzdUsdTicks[20:25]))
	newCorrs.append(getCorr(audUsdTicks[25:], nzdUsdTicks[25:]))

	resultAction = 0 # do nothing

	if AudUsdNzdUsdCorr < -0.7 and AudUsdUsdZarCorr > 0.5 and NzdUsdEurNzdCorr < -0.5:
		minIndex = newCorrs.index(min(newCorrs))

		audTicks = []
		nzdTicks = []

		if minIndex == 0:
			audTicks = audUsdTicks[15:20]
			nzdTicks = nzdUsdTicks[15:20]

		if minIndex == 1:
			audTicks = audUsdTicks[20:25]
			nzdTicks = nzdUsdTicks[20:25]

		if minIndex == 2:
			audTicks = audUsdTicks[25:]
			nzdTicks = nzdUsdTicks[25:]

		emaAudUsdTrendUp = isTrendMovingUp2(audTicks)
		emaAudUsdTrendDown = isTrendMovingDown2(audTicks)

		emaNzdUsdTrendUp = isTrendMovingUp2(nzdTicks)
		emaNzdUsdTrendDown = isTrendMovingDown2(nzdTicks)

		if emaAudUsdTrendUp and emaNzdUsdTrendDown:
			resultAction = -1 # sell

		if emaAudUsdTrendDown and emaNzdUsdTrendUp:
			resultAction = 1 # buy

		if not resultAction == 0:
			print("AUDUSD Up: ", emaAudUsdTrendUp, "AUDUSD Down: ", emaAudUsdTrendDown)
			print("NZDUSD Up: ", emaNzdUsdTrendUp, "NZDUSD Down: ", emaNzdUsdTrendDown)

			print("Prev total corr: ", AudUsdNzdUsdCorrPrev)
			print("Prev corrs:")
			print(prevCorrs)
			print("\n")

			print("Current total corr: ", AudUsdNzdUsdCorr)
			print("Current corrs:")
			print(newCorrs)
			print("\n")

			print("AudUsd + UsdZar Corr:", AudUsdUsdZarCorr)
			print("NzdUsd + EurNzd Corr:", NzdUsdEurNzdCorr)
			print("\n")

			audUsdUpShort, audUsdDownShort = getUnicornIndex(audTicks)
			audUsdUpTotal, audUsdDownTotal = getUnicornIndex(audUsdTicks[-15:])

			nzdUsdUpShort, nzdUsdDownShort = getUnicornIndex(nzdTicks)
			nzdUsdUpTotal, nzdUsdDownTotal = getUnicornIndex(nzdUsdTicks[-15:])

			print("AudUsd up short: ", audUsdUpShort, "AudUsd down short: ", audUsdDownShort)
			print("AudUsd up total: ", audUsdUpTotal, "AudUsd down total: ", audUsdDownTotal)
			print("\n")
			
			print("NzdUsd up short: ", nzdUsdUpShort, "NzdUsd down short: ", nzdUsdDownShort)
			print("NzdUsd up total: ", nzdUsdUpTotal, "NzdUsd down total: ", nzdUsdDownTotal)
			print("\n")

	return resultAction