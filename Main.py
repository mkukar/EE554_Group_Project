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

simTime = 100
timeConstraint = 0.33

mapFileName = "map.txt"
sizeList = []
timeObjects = []
validStartIndexes = []
counter = 0
map = [[Road() for i in range(2)] for j in range(2)] # an array of roads

averageLifespan = 0
carsArrived = 0
totalCars = 0

stoplight_ID_counter = 0

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
	fileIn.close()

	# Scan through outside edges of the map to find all valid starting locations
	for side in range(4):
		if (side == 0):
			# find all valid starting locations on the North side of the map
			for index in range(int(sizeList[0])):
				if (map[index][0].exitDirection == [Constants.DOWN_DIR]):
					validStartIndexes.append([index,0])
		if (side == 1):
			# find all valid starting locations on the South side of the map
			for index in range(int(sizeList[0])):
				if (map[index][int(sizeList[1]) - 1].exitDirection == [Constants.UP_DIR]):
					validStartIndexes.append([index,int(sizeList[1]) - 1])
		if (side == 2):
			# find all valid starting locations on the West side of the map
			for index in range(int(sizeList[1])):
				if (map[0][index].exitDirection == [Constants.RIGHT_DIR]):
					validStartIndexes.append([0,index])
		if (side == 3):
			# find all valid starting locations on the East side of the map
			for index in range(int(sizeList[1])):
				if (map[int(sizeList[0]) - 1][index].exitDirection == [Constants.LEFT_DIR]):
					validStartIndexes.append([int(sizeList[0]) - 1,index])


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
				print 'C',
				#counter += 1
			elif Constants.LEFT_DIR in map[x][y].exitDirection:
				print u'\u2190', # unicode character for left arrow
			elif Constants.RIGHT_DIR in map[x][y].exitDirection:
				print u'\u2192', # unicode character for right arrow
			elif Constants.UP_DIR in map[x][y].exitDirection:
				print u'\u2191',
			elif Constants.DOWN_DIR in map[x][y].exitDirection:
				print u'\u2193',
			elif Constants.NO_DIR in map[x][y].exitDirection:
				print '*',
			else:
				print ' ',
		print
	#print("COUNTER = " + str(counter))



# call this to spawn a car randomly
def spawnCar(carID):
	'''
	# OLD METHOD - requires input startLoc, endLoc, carID, and direction
	global map
	global timeObjects
	global totalCars
	totalCars = totalCars + 1
	map[startLoc[0]][startLoc[1]].isOccupied = True
	timeObjects.append(Car(startLoc,endLoc, carID, direction, map))
	'''

	print 'Spawning car with ID # ', carID

	global map
	global timeObjects
	global totalCars
	global validStartIndexes

	totalCars = totalCars + 1

	tempindexVal = random.randint(0,len(validStartIndexes) - 1)
	tempStartLoc = validStartIndexes[tempindexVal]
	
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

	print "Start Loc: ", tempStartLoc
	print "End Loc: ", tempEndLoc
	print "route: ", tempRoute

	if (map[tempStartLoc[0]][tempStartLoc[1]].isOccupied == False):
		map[tempStartLoc[0]][tempStartLoc[1]].isOccupied = True
		#print("SETTING LOCATION TO OCCUPIED AT " + str(tempStartLoc[0]) + ',' + str(tempStartLoc[1]))
		timeObjects.append(Car(tempStartLoc,tempEndLoc, carID, tempRoute, map))

	# randomly spawn here


# Main

def main():

	global averageLifespan
	global carsArrived
	global map

	print "Initializing map...\n"

	readMap()
	printMap()

	print "Initializing algorithm...\n"
	# initialize algorithm class here
	algo = Algorithm(timeConstraint)

	print "Initialization complete.\n"

	# print "Number of valid start indexes: ", len(validStartIndexes)
	# for x in range(len(validStartIndexes)):
	# 	print validStartIndexes[x]

	'''
	print "DEBUGGING STOPLIGHTS FIRST"
	counter = 0
	carCounter = 0
	for obj in timeObjects:
		if obj.type == "Stoplight":
			print "STOPLIGHT DETECTED WITH COORDINATES " + str(obj.startIndex)
			counter += 1
		elif obj.time == "Car":
			carCounter += 1
	print("TOTAL STOPLIGHTS: " + str(counter))
	print("TOTAL CARS: " + str(carCounter))

	print("CHANGING ONE ROAD IN A SINGLE STOPLIGHT...")
	map[3][3].exitDirection = [Constants.LEFT_DIR]
	print("THIS SHOULD ONLY CHANGE ONE OF THE INTERSECTIONS")
	'''

	print "Simulation Start\n"

	for x in range(simTime): # sim time is how many times to run a simulation tick (1 car length)

		# randomly spawns new cars
		spawnCar(x)
		printMap()
		#print("CAR SPAWN IP")

		# takes a snapshot of the current state and runs the algorithm on it (REAL TIME CONSTRAINED)
		map = algo.calcNextState(map, sizeList)

		# TESTING HEURISTIC ONLY
		heuristicToUse = 1
		print(algo.calc_heuristic(map, sizeList, heuristicToUse, timeObjects))

		for obj in timeObjects:
			if obj.type == "Car":
				obj.setNextLocation()
			#elif obj.type == "Stoplight":
		#		obj.tick()
		for obj in timeObjects:
			if obj.type == "Car":
				res = obj.moveCar()
				if res is True:
					map[obj.currentLoc[0]][obj.currentLoc[1]].isOccupied = False

					print("CAR DESPAWNED. WAS ALIVE FOR " + str(obj.timeAlive))
					averageLifespan += obj.timeAlive
					carsArrived += 1
					timeObjects.remove(obj)

	print "Simulation Complete\n"
	printMap()


if __name__ == "__main__":
	main()