import csv
import random

with open('fixtures_1.csv', 'wb') as csvfile:
    fixtureFile = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for i in range(0, 100000):
    	x1 = random.randint(0, 1)
    	x2 = random.randint(0, 1)
    	y = int(x1 != x2)

    	fixtureFile.writerow([x1, x2, y])

# with open('fixtures_1.csv', 'wb') as csvfile:
#     fixtureFile = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

#     for i in range(0, 100000):
#     	x1 = random.randint(1, 100)
#     	x2 = random.randint(1, 100)
#     	ouput = x1 + x2

#     	fixtureFile.writerow([x1, x2, ouput])