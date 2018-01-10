#Creates 2 quad trees- one with the Starbucks locations and one with Dunkin Donuts locations. Then, it goes through each subway station and counts how many locations are within a certain radius of the station for both quad trees.
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
#Quad tree class and methods 
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


DEGREES_TO_RADIANS = math.pi/180.0
RADIUS_OF_EARTH = 3956

#Measures the distance between two latitude and longitude points 
def flatEarthDistance(lat1, long1, lat2, long2):
    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * DEGREES_TO_RADIANS
    phi2 = (90.0 - lat2) * DEGREES_TO_RADIANS

    # theta = longitude
    theta1 = long1 * DEGREES_TO_RADIANS
    theta2 = long2 * DEGREES_TO_RADIANS
 
    c = math.sqrt(phi1*phi1 + phi2*phi2 - 2*phi1*phi2*math.cos(theta2-theta1))
    return RADIUS_OF_EARTH * c

#range generator which supports floats
def fRange(start, end, incr):
    while float(start) < float(end):
        yield start
        start += float(incr)
        
def main():
    t = QuadTree()
    t2 = QuadTree()
    pts = []
    pts2 = []
    file = open("StarbucksLocations.txt")
    for l in file: #For each line in the Starbucks locations file
        fields = l.split(",")  
        x = float(fields[1].strip()) #Latitude of location
        y = float(fields[0].strip()) #Longitude of location
        data = str()
        t.insert(x, y, data) #Inserts the points into the quad tree
        pts.append((x,y, data))
    file2 = open("DunkinDonutsLocations.txt")
    for l in file2: #For each line in the Dunkin Donuts locations file 
        fields = l.split(",")
        x = float(fields[1].strip())
        y = float(fields[0].strip())
        data = str()
        t2.insert(x,y, data)
        pts2.append((x,y,data)) #Insert lat and longs into a second quad tree
    for i in fRange(.1, .3, .1):
        outputFileDD = open("DDnumbers" + str(i)+ ".txt", "w")
        outputFileS = open("Starbucksnumber" + str(i) + ".txt", "w")
        file2 = open("subwayLocationsAndRidership.txt")
        for line in file2: #For each subway locations which matched the subway ridership file 
                fields = line.split("|")
                lat = float(fields[4].strip())
                longitude = float(fields[5].strip())
                stationName = fields[0]
                stationRidership = fields[2].strip()
                numOfLocations = t.numInRange(lat, longitude,i)
                outputFileS.write(stationName + "|" + stationRidership + "|" + str(numOfLocations) + "|" + fields[6].strip()+ "\n")
                numOfDDLocations = t2.numInRange(lat, longitude, i)
                outputFileDD.write(stationName + "|"  + stationRidership+ "|"+str(numOfDDLocations) + "|"+  fields[6].strip()+ "\n")
    


        

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
