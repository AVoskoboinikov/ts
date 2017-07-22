import csv
import random
import numpy as np

def get_fixtures():
	fixtures = []
	seq_count = 11
	
	seed = 0.001
	seed_step = 0.0001
	item_step = 0.000001

	x = 'xxx'
	
	for _ in range(0, 1000):
		fixtures.append([ np.float32(seed + item * item_step) for item in range(0, seq_count)])
		seed = seed + seed_step

	random.shuffle(fixtures)
	
	return fixtures

with open('fixtures_1.csv', 'wb') as csvfile:
    fixtureFile = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    fixtures = get_fixtures()

    for row in fixtures:
    	fixtureFile.writerow(row)
    

# with open('fixtures_1.csv', 'wb') as csvfile:
#     fixtureFile = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

#     for i in range(0, 100000):
#     	x1 = random.randint(0, 1)
#     	x2 = random.randint(0, 1)
#     	y = int(x1 != x2)

#     	fixtureFile.writerow([x1, x2, y])


# with open('fixtures_1.csv', 'wb') as csvfile:
#     fixtureFile = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

#     for i in range(0, 100000):
#     	x1 = random.randint(0, 1)
#     	x2 = random.randint(0, 1)
#     	y = int(x1 != x2)

#     	fixtureFile.writerow([x1, x2, y])

# with open('fixtures_1.csv', 'wb') as csvfile:
#     fixtureFile = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

#     for i in range(0, 100000):
#     	x1 = random.randint(1, 100)
#     	x2 = random.randint(1, 100)
#     	ouput = x1 + x2

#     	fixtureFile.writerow([x1, x2, ouput])