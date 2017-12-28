import random
import sys
import math
import re
PINF = float('inf')
NINF = -float('inf')
class Node(object):
    def __init__(self, x, y, d):
        self.x = x
        self.y = y
        self.data = [d]
        self.NE = self.SE = self.NW = self.SW = None
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + str(self.data) + ")"
class QuadTree(object):
    def __init__(self):
        self.__root = None
    def insert(self, x, y, d):
        self.__root = self.__insert(self.__root, x, y, d)
    def __insert(self, n, x, y, d):
        if not n: return Node(x, y, d)

        if n.x == x and n.y == y:
            n.data.append(d)
            return n
        if x >= n.x and y >= n.y:
            n.SE = self.__insert(n.SE, x, y, d)
        elif x >= n.x and y < n.y:
            n.NE = self.__insert(n.NE, x, y, d)
        elif x < n.x and y >= n.y:
            n.SW = self.__insert(n.SW, x, y, d)
        else:
            n.NW = self.__insert(n.NW, x, y, d)
        return n
    def numInRange(self, lat1, long1, radius):
        return self.__numInRange(self.__root, lat1, long1, radius)
    def __numInRange(self, n , lat1, long1, radius):
        if not n:
            return 0
        ans = 0
        if circleIntersects(lat1, long1, radius, n.x, PINF, n.y, PINF):
            ans+= self.__numInRange(n.SE, lat1, long1, radius)
        if circleIntersects(lat1, long1, radius, n.x, PINF, NINF, n.y):
            ans+= self.__numInRange(n.NE, lat1, long1, radius)
        if circleIntersects(lat1, long1, radius, NINF, n.x, NINF, n.y):
            ans+= self.__numInRange(n.NW, lat1, long1, radius)
        if circleIntersects(lat1, long1, radius, NINF, n.x, n.y, PINF):
            ans+= self.__numInRange(n.SW, lat1, long1, radius)
        if withinDistance(lat1, long1, n.x, n.y, radius):
            ans+=1
        return ans 

                
def withinDistance(x1, y1, x2, y2, r):
    distance = flatEarthDistance(x1, y1, x2, y2)
    return distance  <= r
def circleIntersects(circleX, circleY, circleR, left, right, top, bot):
    closestX = circleX
    if   circleX < left:  closestX = left
    elif circleX > right: closestX = right

    closestY = circleY
    if   circleY < top: closestY = top
    elif circleY > bot: closestY = bot

    distance = flatEarthDistance(circleX, circleY, closestX, closestY)
    return distance <= circleR  



# Polar Coordinate Flat-Earth Formula
# from http://www.cs.nyu.edu/visual/home/proj/tiger/gisfaq.htm\
    
#
# a = pi/2 - lat1
# b = pi/2 - lat2
# c = sqrt( a^2 + b^2 - 2 * a * b * cos(lon2 - lon1) )
# d = R * c

# Convert latitude and longitude to
# spherical coordinates in radians.
DEGREES_TO_RADIANS = math.pi/180.0
RADIUS_OF_EARTH = 3956

def flatEarthDistance(lat1, long1, lat2, long2):
    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * DEGREES_TO_RADIANS
    phi2 = (90.0 - lat2) * DEGREES_TO_RADIANS

    # theta = longitude
    theta1 = long1 * DEGREES_TO_RADIANS
    theta2 = long2 * DEGREES_TO_RADIANS
 
    c = math.sqrt(phi1*phi1 + phi2*phi2 - 2*phi1*phi2*math.cos(theta2-theta1))
    return RADIUS_OF_EARTH * c

def main():
    t = QuadTree()
    pts = []
    file = open("StarbucksLocations.txt")
    for l in file:
        fields = l.split(",")
        x = float(fields[1].strip())
        y = float(fields[0].strip())
        data = str()
        t.insert(x, y, data)
        pts.append((x,y, data))
    print("Inserted", len(pts), "points into quadtree")
    t2 = QuadTree()
    pts2 = []
    file2 = open("DunkinDonutsLocations.txt")
    for l in file2:
        fields = l.split(",")
        x = float(fields[1].strip())
        y = float(fields[0].strip())
        data = str()
        t2.insert(x,y, data)
        pts2.append((x,y,data))
    print("Inserted", len(pts2), "points into quadtree")
    file2 = open("subwayLocationsAndRidership.txt")
    outputFileDD = open("DDnumbers.txt", "w")
    outputFileS = open("Starbucksnumber.txt", "w")
    hits = 0
    misses = 0
    for line in file2:
        fields = line.split("|")
        lat = float(fields[4].strip())
        longitude = float(fields[5].strip())
        stationName = fields[0]
        stationRidership = fields[2].strip()
        numOfLocations = t.numInRange(lat, longitude,.25)
        outputFileS.write(stationName + "|" + stationRidership + "|" + str(numOfLocations) + "|" + fields[6].strip()+ "\n")
        numOfLocationsBF = BFnumInRange(pts, lat, longitude, .25)
        if numOfLocations == numOfLocationsBF:
            hits+=1
        else:
            misses+=1
        numOfDDLocations = t2.numInRange(lat, longitude, .25)
        outputFileDD.write(stationName + "|"  + stationRidership+ "|"+str(numOfDDLocations) + "|"+  fields[6].strip()+ "\n")
        
    print(hits/(hits+misses)*100)
def BFnumInRange(sbLocations, lat, lng, radius):
    count = 0
    for s in sbLocations:
        if flatEarthDistance(s[0], s[1], lat, lng) <= radius:
            count+=1
    return count



        

if __name__ == '__main__':
    main()
                                                                                                                                                                                                                              
    #tree = QuadTree()
    #i = tree.insert(54, 68, 2)
    #print(i)
    #file = open("StarbucksLocations.txt")
    #for l in file:
        #fields = l.split(",")
        #j = tree.insert(float(fields[0].strip()), float(fields[1].strip()), 1)
        #print(j)
#if __name__ == "__main__": main()
