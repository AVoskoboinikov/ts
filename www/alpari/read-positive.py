import csv
import pandas as pd

audusdFile = 'AUDUSD1M.csv'
fileToWrite = 'AUDUSD-positive.csv'

audusd = pd.read_csv(audusdFile, usecols=['Date', 'Time', 'Open'])
openAudUsd = audusd['Open'].values

del audusd

fixtureSize = len(openAudUsd)
sampleSize = 30
lagSize = 10
allowedDiff = 0.001

fixtures = []

for startFrom in range(fixtureSize - sampleSize - lagSize):
	x1 = openAudUsd[startFrom + sampleSize - 1]
	x2 = openAudUsd[startFrom + sampleSize + lagSize - 1]
	diff = float(x2) - float(x1)
	label = int(diff >= allowedDiff)

	if (label == 1):
		xFrom = startFrom
		xTo = startFrom + sampleSize + lagSize
		fixtures.append(openAudUsd[xFrom:xTo])

print(len(fixtures))

with open(fileToWrite, 'w', newline='') as csvfile:
	destination = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	destination.writerows(fixtures)