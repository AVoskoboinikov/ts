import csv
import pandas as pd

# audusdFile = 'AUDUSD1M - last year.csv'
# nzdusdFile = 'NZDUSD1M - last year.csv'
audusdFile = 'AUDUSD1M.csv'
nzdusdFile = 'NZDUSD1M.csv'
fileToWrite = 'AUDUSD-NZDUSD-1M-3.csv'

audusd = pd.read_csv(audusdFile, usecols=['Date', 'Time', 'Open'])
audusd.rename(columns={'Open':'Open AUDUSD'}, inplace=True)
audusd['Date Time'] = audusd['Date'].map(str) + ':' + audusd['Time'].map(str)
audusd.set_index('Date Time', inplace=True)
del audusd['Date']
del audusd['Time']

nzdusd = pd.read_csv(nzdusdFile, usecols=['Date', 'Time', 'Open'])
nzdusd.rename(columns={'Open':'Open NZDUSD'}, inplace=True)
nzdusd['Date Time'] = nzdusd['Date'].map(str) + ':' + nzdusd['Time'].map(str)
nzdusd.set_index('Date Time', inplace=True)
del nzdusd['Date']
del nzdusd['Time']

audnzd = audusd.join(nzdusd, how='inner')
audnzd.reset_index(inplace=True)

openAudUsd = audnzd['Open AUDUSD'].values
openNzdUsd = audnzd['Open NZDUSD'].values

del audusd
del nzdusd
del audnzd

fixtureSize = len(openAudUsd)
sampleSize = 30
lagSize = 10
allowedDiff = 0.001

fixtures = []
positiveFixtures = []
negativeFixtures = []

for startFrom in range(fixtureSize - sampleSize - lagSize):
	sample = []

	x1 = openAudUsd[startFrom + sampleSize - 1]
	x2 = openAudUsd[startFrom + sampleSize + lagSize - 1]
	diff = float(x2) - float(x1)
	label = int(diff >= allowedDiff)

	if (label == 1) or (label == 0 and len(positiveFixtures) > len(negativeFixtures)):
		for i in range(sampleSize):
			j = startFrom + i

			sample.append(round(float(openAudUsd[j]), 4))
			sample.append(round(float(openNzdUsd[j]), 4))

		if label == 0:
			sample.append(1)
			sample.append(0)
			negativeFixtures.append(sample)

		if label == 1:
			sample.append(0)
			sample.append(1)
			positiveFixtures.append(sample)

for i in range(len(positiveFixtures)):
	fixtures.append(positiveFixtures[i])
	fixtures.append(negativeFixtures[i])


print(len(positiveFixtures))
print(len(negativeFixtures))
print(len(fixtures))

with open(fileToWrite, 'w', newline='') as csvfile:
	destination = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	destination.writerows(fixtures)