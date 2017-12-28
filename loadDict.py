import re

file = open("subwayRankings.txt")
prevLat = ""
file3 = open("subwayLocationsAndRidership.txt", "w")
for line in file:
    fields = line.split("|")
    stationName = fields[0]
    file2 = open("subwayentrancesaltered.txt")
    for line2 in file2:
        fields2 = line2.split(",")
        arr = []
        parts = [2]
        parts[0] = ""
        parts2 = [2]
        parts2[0] = ""
        for i in range(3, 13):
            arr.append(fields2[i])
        if re.search(r'-', fields2[0]):
            parts = re.split(r'-', fields2[0])
        if re.search(r'-', fields[0]):
            parts2 = re.split(r'-', fields[0])
        if re.match(r""+fields2[0]+"" , stationName) or re.match(r""+stationName+"", fields2[0]) or (parts[0] != "" and re.search(r''+parts[0]+'', stationName) and re.search(r''+parts[1]+'', stationName)) or (parts2[0] != "" and re.search(r''+parts2[0]+'', fields2[0]) and re.search(r''+parts2[1]+'', fields2[0])):
            if fields[1] in arr and fields2[1] != prevLat:
                fields3 = fields[2].split(",")
                if len(fields3) == 2:
                    ridership = fields3[0] + fields3[1]
                else:
                    ridership = fields3[0]
                file3.write(fields[0]+"|"+ fields[1]+"|"+ ridership+"|"+fields2[0]+"|"+fields2[1]+"|"+fields2[2]+"|"+ fields[3].strip() + "\n")
                prevLat = fields2[1]

                
        
             
