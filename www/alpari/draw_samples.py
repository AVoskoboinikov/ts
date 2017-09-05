from shutil import copyfile
import matplotlib.pyplot as plt
import time
import os
import numpy as np
import hashlib
from get_unicorn_index import getUnicornIndex

fixture_file = 'AUDUSD-hypothesis.csv'

with open(fixture_file) as source:
    for row in source:
        arr = row.strip().split(',')
        
        y_axis = [float(item) for item in arr]
        y2_axis = y_axis[50:60]

        x_axis = [i for i in range(1, len(y_axis) + 1)]
        x2_axis = [i for i in range(51, 61)]

        # up, down = getUnicornIndex(y_axis)
        # if down > up or abs(up - down) < 0.0005:
        # 	continue

        # print(up)
        # print(down)
        # print("\n\n")

        plt.plot(x_axis, y_axis, 'g-')
        plt.plot(x2_axis, y2_axis, 'b-')
        # plt.show()
        plotFileName = hashlib.md5(row.encode("utf")).hexdigest() + '.png'
        plt.savefig('../plots/' + plotFileName)
        plt.clf()