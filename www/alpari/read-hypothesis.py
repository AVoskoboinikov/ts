import csv
import pandas as pd
from find_unicorns import findUnicorns
from get_unicorn_index import getUnicornIndex

audusdFile = 'AUDUSD1M - last year.csv'
fileToWrite = 'AUDUSD-hypothesis.csv'

audusd = pd.read_csv(audusdFile, usecols=['Date', 'Time', 'Open'])
openAudUsd = audusd['Open'].values

del audusd

fixtureSize = len(openAudUsd)
howMany = 0
fixtures = []

for startFrom in range(50, fixtureSize - 50):
	sample = []
	

	# check w-shape + 3 steps

	# x1 = openAudUsd[startFrom]
	# x2 = openAudUsd[startFrom + 1]
	# x3 = openAudUsd[startFrom + 2]
	# x4 = openAudUsd[startFrom + 3]
	# x5 = openAudUsd[startFrom + 4]
	# x6 = openAudUsd[startFrom + 5]
	# x7 = openAudUsd[startFrom + 6]
	# x8 = openAudUsd[startFrom + 7]

	# if (x2 < x1):
	# 	if (x3 < x1 and x3 > x2 and x4 < x3 and abs(x3 - x2) >= 0.0001 and abs(x4 - x3) >= 0.0001):
	# 		if abs(x4 - x2) < 0.0001:
	# 			if (x5 > x3):
	# 				up, down = findUnicorns(openAudUsd[startFrom + 4 : startFrom + 11])
					
	# 				if down == sorted(down) and len(down) >= 3 and down[0] > x4 and abs(down[0] - x4) > 0.0001:
	# 					sample = openAudUsd[ (startFrom - 30) : (startFrom + 30) ]
	# 					fixtures.append(sample)

	up, down = findUnicorns(openAudUsd[startFrom: startFrom + 10])
	
	if down == sorted(down) and len(down) >= 3:
		ok = True
		
		for i in range(1, len(down)):
			if abs(down[i] - down[i-1]) <= 0:
				ok = False
		
		if ok:
			up, down = findUnicorns(openAudUsd[startFrom - 20: startFrom])
			
			if down == sorted(down, reverse=True):
				ok = False

		if ok:
			up, down = getUnicornIndex(openAudUsd[startFrom - 20: startFrom])

			if down > up or abs(up - down) < 0.0005:
				ok = False

		if ok:
			up, down = findUnicorns(openAudUsd[startFrom: startFrom + 10])
			sortedUp = sorted(up)
			sortedDown = sorted(down)

			x1 = sortedDown[0]
			x2 = sortedUp[-1]

			if abs(x2 - x1) >= 0.0005:
				ok = False

		if ok:
			sample = openAudUsd[ (startFrom - 50) : (startFrom + 50) ]
			fixtures.append(sample)
	
	if (len(fixtures) >= 300):
		break;

# print(howMany)
# print(len(fixtures))

with open(fileToWrite, 'w', newline='') as csvfile:
	destination = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	destination.writerows(fixtures)