import csv
import random

with open('fixtures_1.csv', 'wb') as csvfile:
    fixtureFile = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for i in range(0, 5000):
    	x1 = random.randint(1, 10000)
    	x2 = random.randint(1, 10000)
    	ouput = x1 + x2

    	fixtureFile.writerow([x1, x2, ouput])

with open('fixtures_2.csv', 'wb') as csvfile:
    fixtureFile = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for i in range(0, 5000):
    	x1 = random.randint(1, 10000)
    	x2 = random.randint(1, 10000)
    	ouput = x1 + x2

    	fixtureFile.writerow([x1, x2, ouput])

with open('fixtures_3.csv', 'wb') as csvfile:
    fixtureFile = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for i in range(0, 5000):
    	x1 = random.randint(1, 10000)
    	x2 = random.randint(1, 10000)
    	ouput = x1 + x2

    	fixtureFile.writerow([x1, x2, ouput])