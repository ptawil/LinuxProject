#Running make in mosh doesn't work because of the plot pdf's that are created but it works in x2go. 
all: StarbucksLocations.txt DunkinDonutsLocations.txt subwayentrances.txt subwayRankings.txt subwayentrancesaltered.txt subwayLocationsAndRidership.txt DDnumbers0.1.txt DDnumbers0.2.txt Starbucksnumber0.1.txt Starbucksnumber0.2.txt plot0.1.pdf plot0.2.pdf

clean:
	rm StarbucksLocations.txt DunkinDonutsLocations.txt subwayentrances.txt subwayRankings.txt subwayentrancesaltered.txt subwayLocationsAndRidership.txt DDnumbers0.1.txt DDnumbers0.2.txt Starbucksnumber0.1.txt Starbucksnumber0.2.txt

StarbucksLocations.txt: Starbucks.csv
	cat Starbucks.csv | grep NY | cut -d ',' -f 2,1 > StarbucksLocations.txt
DunkinDonutsLocations.txt: DunkinDonuts.csv
	cat DunkinDonuts.csv | grep NY | cut -d ',' -f 2,1  > DunkinDonutsLocations.txt
subwayentrances.txt: NYCSubwayData
	cat NYCSubwayData | cut -d ',' -f 3,4,5,6,7,8,9,10,11,12,13,14,15,16 | sort | uniq > subwayentrances.txt 

subwayentrancesaltered.txt: subwayentrances.txt convertSubwayData.py
	python3 convertSubwayData.py

subwayRankings.txt: subwayRidership.py
	python3 subwayRidership.py

subwayLocationsAndRidership.txt: matchRidership.py subwayentrancesaltered.txt
	python3 matchRidership.py

DDnumbers0.1.txt DDnumbers0.2.txt Starbucksnumber0.1.txt Starbucksnumber0.2.txt: quadTree.py subwayLocationsAndRidership.txt StarbucksLocations.txt DunkinDonutsLocations.txt 
	python3 quadTree.py

plot0.1.pdf plot0.2.pdf: plot.py DDnumbers0.1.txt DDnumbers0.2.txt Starbucksnumber0.1.txt Starbucksnumber0.2.txt 
	python3 plot.py

