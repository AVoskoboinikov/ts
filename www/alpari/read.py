import csv

fileToRead = 'AUDUSD1H.csv'
fileToWrite = 'test2.csv'

with open(fileToRead) as source:
	date_values = []
	time_values = []
	open_values = []
	high_values = []
	low_values = []
	close_values = []

	for row in source:
		date_value, time_value, open_value, high_value, low_value, close_value, _ = row.split(',')

		date_values.append(date_value)
		time_values.append(time_value)
		open_values.append(open_value)
		high_values.append(high_value)
		low_values.append(low_value)
		close_values.append(close_value)

windowSize = 23
lag = 1

fixtureSize = len(date_values) - (windowSize + lag)

with open(fileToWrite, 'w', newline='') as csvfile:
	destination = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for i in range(fixtureSize):
		row = open_values[i:(i+windowSize)]
		row.append(open_values[i+windowSize+lag-1])

		deltas = []
		
		for j in range(len(row)):
			if j == 0:
				deltas.append(row[j])
			else:
				delta = round(float(row[j]) - float(row[j-1]), 5)
				deltas.append(delta)

		destination.writerow(deltas)