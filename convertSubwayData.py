#Makes substitutions in the station names of the subway entrance location file so that it matches up with the names of the subway stations in the subway ridership chart and writes it to a file called subwayentrancesaltered.txt. 

import re

file = open("subwayentrances.txt")
data = file.read()
data = re.sub("th ", " ", data)
data = re.sub("3rd", "3", data)
data = re.sub("2nd", "2", data)
data = re.sub("1st", "1", data)
data = re.sub("Parkway", "Pkwy", data)
data = re.sub("Highway", "Hwy", data)
data = re.sub(" - ", "-", data)
data = re.sub("Square", "Sq", data)
data = re.sub("Place", "Pl", data)
data = re.sub(" & ", "-", data)
data = re.sub("Sou", "South", data)
data = re.sub("Kosciusko", "Kosciuszko", data)
data = re.sub("N,R,", "W,R,", data)
data = re.sub(",H,", ",A,H,", data)
file = open("subwayentrances.txt", "w")
file.write(data)
file = open("subwayentrances.txt")
file2 = open("subwayentrancesaltered.txt", "w")
prevName = ""
prevLine = ""
#only writes the lines to the file which are distinct subway stations-ifthe station has the same name and same first subway line, then it is assumed to be the same station and is omitted, otherwise it is written.
for line in file:
    fields=line.split(",")
    if fields[0] != prevName or fields[3] != prevLine:
        prevName = fields[0]
        prevLine = fields[3]
        file2.write(line)        
