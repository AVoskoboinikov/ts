import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates
import datetime

def readFile(FileName, pair):
	data = pd.read_csv(FileName, usecols=['Date', 'Time', 'Open'], index_col=False)
	data.rename(columns={'Open':'Open ' + pair}, inplace=True)
	data['Date Time'] = data['Date'].map(str) + ' ' + data['Time'].map(str)
	data.set_index('Date Time', inplace=True)
	del data['Date']
	del data['Time']

	return data

def getAudAndNzdTicks():
	fileToReadAUD = 'history/AUDUSD.csv'
	fileToReadNZD = 'history/NZDUSD.csv'

	audusd = readFile(fileToReadAUD, 'AUDUSD')
	nzdusd = readFile(fileToReadNZD, 'NZDUSD')

	joined = audusd.join(nzdusd, how='inner')
	joined = joined.fillna(0)
	# joined.reset_index(inplace=True)

	# print(joined.head())
	# print(joined.loc['2017.02.01':'2017.03.01'])

	# return joined['Open AUDUSD'].values, joined['Open NZDUSD'].values

	return joined

print('reading data...')

df = getAudAndNzdTicks()
period = 15

print('analyzing data...')

for month in range(12, 13):
	dateFrom = '2017.' + str("%02d" % (month,)) + '.01'
	dateTo = '2017.' + str("%02d" % (month+1,)) + '.01'
	monthDf = df.loc[dateFrom:dateTo]
	monthDf.reset_index(inplace=True)

	monthCorrs = []
	monthDates = []

	print('analyzing ' + dateFrom + ' - ' + dateTo)

	print(monthDf.head())
	print(monthDf.tail())

	for tick in range(0, (len(monthDf) - period), 45):
		monthCorrs.append(monthDf.iloc[tick:tick + period].corr()['Open AUDUSD']['Open NZDUSD'])
		monthDates.append(monthDf.iloc[tick]['Date Time'])

	print(monthDates)

	y_axis = monthCorrs
	# x_axis = [i for i in range(1, len(monthCorrs) + 1)]
	convertedDates = map(datetime.datetime.strptime, monthDates, len(monthDates)*['%Y.%m.%d %H:%M'])
	x_axis = [dates.date2num(date) for date in convertedDates]
	
	plotTitle = str(period) + ' - ' + dateFrom + ' - ' + dateTo

	fig = plt.figure()
	fig.set_size_inches(15,8)
	fig.canvas.set_window_title(plotTitle)

	plt.plot(x_axis, y_axis, 'g-')
	plt.ylabel(plotTitle)

	ax = plt.gcf().axes[0] 
	ax.xaxis.set_major_formatter(dates.DateFormatter('%Y.%m.%d %H:%M'))
	# plt.gcf().autofmt_xdate(rotation=25)


	plt.figtext(0.025, 0.975, "Avg Corr: " + str(format(sum(monthCorrs)/len(monthCorrs), 'f')), color="black", weight=500, size="medium")

	plt.grid()

	plt.show()
	# plt.savefig('../plots/corrs/' + plotTitle + '.png')

	plt.clf()
	plt.close(fig)

	print('...done')