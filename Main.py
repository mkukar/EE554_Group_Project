# Main.py
# New main incorporating overall algorithm class
# EE554 Group Project
# Spring 2017

from Road import *
from Car import *
from Stoplight import *
from TimeObject import *
import Constants
from Algorithm import *
import random

# #
# global variables
# #

pSpawnNorth = 0.25
pSpawnSouth = 0.25
pSpawnWest = 0.25
pSpawnEast = 0.25


maxCarCounter = 20
totalCars = 0
simTimeCounter = 0
timeConstraint = 0.33
heuristicToUse = 2

mapFileName = "map.txt"
sizeList = []
timeObjects = []
validStartIndexesNorth = []
validStartIndexesSouth = []
validStartIndexesWest = []
validStartIndexesEast = []
counter = 0
map = [[Road() for i in range(2)] for j in range(2)] # an array of roads

carsArrived = 0
totalCars = 0

stoplight_ID_counter = 0

timerFinishedBool = False

W  = '\033[0m'  # Default (White/Black) (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
Wh = '\033[37m' # WHITE

BG_BLACK = '\033[40m'
BG_RED = '\033[41m'
BG_BLUE = '\033[44m'

# #
# functions
# #

def readMap():
	global map
	global mapFileName
	global sizeList
	global validStartIndexes
	global stoplight_ID_counter

	fileIn = open(mapFileName, 'r') # double check this
	sizeList = fileIn.readline().strip().split(',')
	# copies the entire file into a 2-d array that we can read from sequentially
	# modified this way to handle the stoplight class searching for 'S' objects in 2 dimensions
	strMap = [[' ' for y in range(int(sizeList[1]))] for x in range(int(sizeList[0]))]
	map = [[Road() for i in range(int(sizeList[1]))] for j in range(int(sizeList[0]))]
	for y in range(int(sizeList[1])):
		line = fileIn.readline().upper()
		for x in range(int(sizeList[0])):
			strMap[x][y] = str(line[x])
			map[x][y].location = [x,y]
			# initializes only the roads UDLR*, ignores S
			if (strMap[x][y] == 'U'):
				map[x][y].exitDirection = [Constants.UP_DIR]
			elif (strMap[x][y] == 'D'):
				map[x][y].exitDirection = [Constants.DOWN_DIR]
			elif (strMap[x][y] == 'L'):
				map[x][y].exitDirection = [Constants.LEFT_DIR]
			elif (strMap[x][y] == 'R'):
				map[x][y].exitDirection = [Constants.RIGHT_DIR]
			elif (strMap[x][y] == '*'):
				map[x][y].exitDirection = [Constants.NO_DIR]
			else:
				map[x][y].exitDirection = [Constants.NO_DIR]
				map[x][y].partOfIntersection = True # only other case is that it is part of an intersection
	fileIn.close()

	# Scan through outside edges of the map to find all valid starting locations
	for side in range(4):
		if (side == 0):
			# find all valid starting locations on the North side of the map
			for index in range(int(sizeList[0])):
				if (map[index][0].exitDirection == [Constants.DOWN_DIR]):
					validStartIndexesNorth.append([index,0])
		if (side == 1):
			# find all valid starting locations on the South side of the map
			for index in range(int(sizeList[0])):
				if (map[index][int(sizeList[1]) - 1].exitDirection == [Constants.UP_DIR]):
					validStartIndexesSouth.append([index,int(sizeList[1]) - 1])
		if (side == 2):
			# find all valid starting locations on the West side of the map
			for index in range(int(sizeList[1])):
				if (map[0][index].exitDirection == [Constants.RIGHT_DIR]):
					validStartIndexesWest.append([0,index])
		if (side == 3):
			# find all valid starting locations on the East side of the map
			for index in range(int(sizeList[1])):
				if (map[int(sizeList[0]) - 1][index].exitDirection == [Constants.LEFT_DIR]):
					validStartIndexesEast.append([int(sizeList[0]) - 1,index])


	for y in range(int(sizeList[1])):
		for x in range(int(sizeList[0])):

			# handles creating a stoplight group and will automatically write to the rest of the road objects after called
			if (strMap[x][y] == 'S'):
				# main class determines the stoplight size because it has access to the actual file input
				xSize = 0
				ySize = 0
				xScan = x
				yScan = y
				# checks all the x indices
				while strMap[xScan][yScan] == 'S':
					xSize = 0
					while strMap[xScan][yScan] == 'S':
						strMap[xScan][yScan] = '*'
						xSize = xSize + 1
						xScan = xScan + 1
					xScan = x
					ySize = ySize + 1
					yScan = yScan + 1

				#print("DETECTED A STOPLIGHT OF SIZE (" + str(xSize) + "," + str(ySize) + ")")
				#if len(timeObjects) <= 24:
				#	print("CREATED STOPLIGHT - ERASE THIS LATER FOR DEBUG in Main.py L115")
				#	print("x - " + str(x) + " y - " + str(y) + " xSize - " + str(xSize) + " ySize - " + str(ySize))
				timeObjects.append(Stoplight(map, x, y,xSize,ySize, stoplight_ID_counter))
				stoplight_ID_counter += 1 # keeps track of unique IDs


def printMap():
	#counter = 0
	# new printing method uses unicode + overlays the cars directly on the road
	for y in range(int(sizeList[1])):
		for x in range(int(sizeList[0])):
			# print map[x][y].exitDirection
			if map[x][y].isOccupied:
				print 'C'+W,
				#counter += 1
			elif Constants.LEFT_DIR in map[x][y].exitDirection:
				print B+u'\u2190'+W, # unicode character for left arrow
			elif Constants.RIGHT_DIR in map[x][y].exitDirection:
				print B+u'\u2192'+W, # unicode character for right arrow
			elif Constants.UP_DIR in map[x][y].exitDirection:
				print R+u'\u2191'+W,
			elif Constants.DOWN_DIR in map[x][y].exitDirection:
				print R+u'\u2193'+W,
			elif Constants.NO_DIR in map[x][y].exitDirection:
				print Wh+'*'+W,
			else:
				print ' ',
				pass
		print
	#print("COUNTER = " + str(counter))



# call this to spawn a car randomly
def spawnCar(carID, counterIn):
	'''
	# OLD METHOD - requires input startLoc, endLoc, carID, and direction
	global map
	global timeObjects
	global totalCars
	totalCars = totalCars + 1
	map[startLoc[0]][startLoc[1]].isOccupied = True
	timeObjects.append(Car(startLoc,endLoc, carID, direction, map))
	'''

	#print 'Spawning car with ID # ', carID

	global map
	global timeObjects
	global totalCars
	global validStartIndexesNorth
	global validStartIndexesSouth
	global validStartIndexesWest
	global validStartIndexesEast

	totalCars = totalCars + 1
	tempSpawnSide = random.uniform(0,1)

	if tempSpawnSide >= 0 and tempSpawnSide < pSpawnNorth:
		# Spawn on North Side
		tempindexVal = random.randint(0,len(validStartIndexesNorth) - 1)
		tempStartLoc = validStartIndexesNorth[tempindexVal]
	elif tempSpawnSide >= pSpawnNorth and tempSpawnSide < (pSpawnNorth + pSpawnSouth):
		# Spawn on South Side
		tempindexVal = random.randint(0,len(validStartIndexesSouth) - 1)
		tempStartLoc = validStartIndexesSouth[tempindexVal]
	elif tempSpawnSide >= (pSpawnNorth + pSpawnSouth) and tempSpawnSide < (pSpawnNorth + pSpawnSouth + pSpawnWest):
		# Spawn on West Side
		tempindexVal = random.randint(0,len(validStartIndexesWest) - 1)
		tempStartLoc = validStartIndexesWest[tempindexVal]
	elif tempSpawnSide >= (pSpawnNorth + pSpawnSouth + pSpawnWest) and tempSpawnSide <= 1:
		# Spawn on East side
		tempindexVal = random.randint(0,len(validStartIndexesEast) - 1)
		tempStartLoc = validStartIndexesEast[tempindexVal]
	
	
	# calculate the end location and route of the new car
	if Constants.UP_DIR in map[tempStartLoc[0]][tempStartLoc[1]].exitDirection:
		tempEndLoc = [tempStartLoc[0], tempStartLoc[1] - (int(sizeList[1]) - 1)]
		tempRoute = [Constants.UP_DIR] * int(sizeList[1])
	elif Constants.DOWN_DIR in map[tempStartLoc[0]][tempStartLoc[1]].exitDirection:
		tempEndLoc = [tempStartLoc[0], tempStartLoc[1] + (int(sizeList[1]) - 1)]
		tempRoute = [Constants.DOWN_DIR] * int(sizeList[1])
	elif Constants.LEFT_DIR in map[tempStartLoc[0]][tempStartLoc[1]].exitDirection:
		tempEndLoc = [tempStartLoc[0] - (int(sizeList[0]) - 1), tempStartLoc[1]]
		tempRoute = [Constants.LEFT_DIR] * int(sizeList[0])
	elif Constants.RIGHT_DIR in map[tempStartLoc[0]][tempStartLoc[1]].exitDirection:
		tempEndLoc = [tempStartLoc[0] + (int(sizeList[0]) - 1), tempStartLoc[1]]
		tempRoute = [Constants.RIGHT_DIR] * int(sizeList[0])

	#print "Start Loc: ", tempStartLoc
	#print "End Loc: ", tempEndLoc
	#print "route: ", tempRoute

	if (map[tempStartLoc[0]][tempStartLoc[1]].isOccupied == False):
		map[tempStartLoc[0]][tempStartLoc[1]].isOccupied = True
		#print("SETTING LOCATION TO OCCUPIED AT " + str(tempStartLoc[0]) + ',' + str(tempStartLoc[1]))
		timeObjects.append(Car(tempStartLoc,tempEndLoc, carID, tempRoute, map))
		counterIn += 1


	# randomly spawn here

	return counterIn

def timerFinished():
	global timerFinishedBool
	timerFinishedBool = True
	print("TIMER FINISHED")

# Main

def main():

	global carsArrived
	global map
	global simTimeCounter
	global totalCars
	global timerFinishedBool
	global pSpawnNorth
	global pSpawnSouth
	global pSpawnWest
	global pSpawnEast

	seed_val = 1
	sim_counter = 0

	print("MAP INFO:")
	print("X SIZE: " + str(len(map)))
	print("Y SIZE: " + str(len(map[:])))

	simulation_list = []
	with open('simulations.txt', 'r') as in_file:

		for line in in_file:
			# Skip comment lines which are designated with '#'
			if line[:1] == '#':
				continue
			# skip empty lines
			if not line.strip():
				continue

			simulation_list.append(line.strip().split(','))

	print simulation_list

	outfile = open('simulation_results.txt', 'w')

	print "Initialization complete.\n"

	print "Simulation Start\n"

	for simulation in simulation_list:
		sim_counter += 1

		pSpawnNorth = float(simulation[0])
		pSpawnSouth = float(simulation[1])
		pSpawnEast = float(simulation[2])
		pSpawnWest = float(simulation[3])
		carsPerSec = int(simulation[4])
		maxCarCounter = int(simulation[5])


		seed_val += 100
		print "Seeding Random Number Generator with " + str(seed_val)
		random.seed(seed_val)

		outfile.write('Simulation ' + str(sim_counter) + ' with seed #: ' + str(seed_val) + '\n')
		outfile.write('\tSpawning probabilities: ' + str([pSpawnNorth,pSpawnSouth,pSpawnEast,pSpawnWest]) + '\n')


		print "Running simulation with spawning probabilities", [pSpawnNorth,pSpawnSouth,pSpawnEast,pSpawnWest]

		# algoModeOn = False

		for i in range(2):
			carsDespawnCounter = 0
			carsSpawnCounter = 0
			averageLifespan = 0
			carsArrived = 0

			print "Initializing map...\n"

			readMap()
			printMap()

			print "Initializing algorithm...\n"
			# initialize algorithm class here
			algo = Algorithm(timeConstraint)

			if i == 0:
				algoModeOn = False # turn to FALSE to use normal timer mode
				print "ALGORITHM OFF"
				outfile.write('\t\tAlgorithm OFF:\n')
			elif i == 1:
				algoModeOn = True
				print "ALGORITHM ON"
				outfile.write('\t\tAlgorithm ON:\n')

			while(carsDespawnCounter < maxCarCounter): # sim time is how many times to run a simulation tick (1 car length)

				print("Cars Despawned: " + str(carsDespawnCounter))
				simTimeCounter += 1

				# randomly spawns new cars until carSpawnCounter == totalCars
				for y in range(carsPerSec):
					if carsSpawnCounter < maxCarCounter:
						carsSpawnCounter = spawnCar(simTimeCounter + (y*carsPerSec), carsSpawnCounter)
				printMap()

				map = algo.calcNextState(map, sizeList, heuristicToUse, timeObjects)

				for obj in timeObjects:
					if obj.type == "Car":
						obj.setNextLocation()
					elif obj.type == "Stoplight":
						obj.tick(algoModeOn) # TRUE to use algorithm mode
				for obj in timeObjects:
					if obj.type == "Car":
						res = obj.moveCar()
						if res is True:
							carsDespawnCounter += 1
							map[obj.currentLoc[0]][obj.currentLoc[1]].isOccupied = False

							#print("CAR DESPAWNED. WAS ALIVE FOR " + str(obj.timeAlive))
							averageLifespan += obj.timeAlive
							carsArrived += 1
							timeObjects.remove(obj)

			print "Simulation Complete\n"
			printMap()

			print("AVERAGE CAR LIFESPAN: ")
			outfile.write('\t\t\tAverage Car Lifespan: ')
			if carsArrived > 0:
				print(averageLifespan/carsArrived)
				outfile.write(str(averageLifespan/carsArrived) + '\n')
			else:
				print("0")
				outfile.write('0')
			print("CARS ARRIVED: " + str(carsDespawnCounter))


if __name__ == "__main__":
	main()


