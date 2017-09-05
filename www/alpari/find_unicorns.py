# 10, 6, 11
# x = [2, 3, 4, 10, 8, 6, 7, 7, 9, 11, 10, 7, 4]

def findUnicorns(breadCrumbs):
	upUnicorns = []
	downUnicorns = []
	
	direction = ''

	for i in range(1, len(breadCrumbs)):
		if breadCrumbs[i] > breadCrumbs[i-1]:
			newDirection = 'up'

		if breadCrumbs[i] < breadCrumbs[i-1]:
			newDirection = 'down'

		if breadCrumbs[i] == breadCrumbs[i-1]:
			newDirection = 'stay'

		if direction == '' or direction == 'stay':
			direction = newDirection
			continue

		if newDirection != direction:
			if newDirection == 'up':
				downUnicorns.append(breadCrumbs[i-1])

			if newDirection == 'down':
				upUnicorns.append(breadCrumbs[i-1])

		direction = newDirection

	return upUnicorns, downUnicorns

# up, down = findUnicorns(x)

# print(up)
# print(down)