#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
import math

file = open("DDnumbers.txt")
x = list()
y = list()
x1 = list()
y1 = list()
for line in file:
    fields = line.split("|")
    x.append(int(fields[3]))
    y.append(int(fields[2]))
file2 = open("Starbucksnumber.txt")
for line in file2:
    fields = line.split("|")
    x1.append(int(fields[3]))
    y1.append(int(fields[2]))
plt.scatter(x,y, c = 'b', alpha = .7)
plt.scatter(x1, y1, c='m', alpha = .7)
plt.xlabel("Subway Weekday Ridership")
plt.ylabel("Quantity of DD Locations Within Range of .3 miles")
plt.show()
