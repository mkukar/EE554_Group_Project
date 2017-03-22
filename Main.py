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

# #
# global variables
# #

simTime = 100
timeConstraint = 0.33

mapFileName = "map.txt"
sizeList = []
timeObjects = []
counter = 0
map = [[Road() for i in range(2)] for j in range(2)] # an array of roads

averageLifespan = 0
carsArrived = 0
totalCars = 0

# #
# functions
# #

def readMap():
	global map
	global mapFileName
	global sizeList
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

				# print("DETECTED A STOPLIGHT OF SIZE (" + str(xSize) + "," + str(ySize) + ")")
				timeObjects.append(Stoplight(map, x, y,xSize,ySize))


def printMap():

	# new printing method uses unicode + overlays the cars directly on the road
	for y in range(int(sizeList[1])):
		for x in range(int(sizeList[0])):
			# print map[x][y].exitDirection
			if map[x][y].isOccupied == True:
				print 'C',
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

	print("IP")

	global map
	global timeObjects
	global totalCars

	totalCars = totalCars + 1

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


	print "Simulation Start\n"

	for x in range(simTime): # sim time is how many times to run a simulation tick (1 car length)

		# randomly spawns new cars
		print("CAR SPAWN IP")

		# takes a snapshot of the current state and runs the algorithm on it (REAL TIME CONSTRAINED)
		map = algo.calcNextState(map)

		# moves cars
		for x in range(simTime):
			for obj in timeObjects:
				if obj.type == "Car":
					obj.setNextLocation()
			for obj in timeObjects:
				if obj.type == "Car":
					res = obj.moveCar()
					if res is True:
						map[obj.currentLoc[0]][obj.currentLoc[1]].isOccupied = False

						#print("CAR DESPAWNED. WAS ALIVE FOR " + str(obj.timeAlive))
						averageLifespan += obj.timeAlive
						carsArrived += 1
						timeObjects.remove(obj)

	print "Simulation Complete\n"
	printMap()


if __name__ == "__main__":
	main()