# Main.py
# EE554 Group Project
# Spring 2017

from Road import *
from Car import *
from TimeObject import *
import Constants

# #
# global variables
# #

mapFileName = "map.txt"
sizeList = []
activeCars = []
timeObjects = []
counter = 0
map = [[Road() for i in range(2)] for j in range(2)] # an array of roads

# #
# functions
# #

def readMap():
	global map
	global mapFileName
	global sizeList
	fileIn = open(mapFileName, 'r') # double check this
	sizeList = fileIn.readline().strip().split(',')
	print(sizeList)
	map = [[Road() for i in range(int(sizeList[1]))] for j in range(int(sizeList[0]))]
	for y in range(int(sizeList[1])):
		#print y
		line = fileIn.readline().upper()
		for x in range(int(sizeList[0])):
			#print "," + str(x)
			map[x][y].location = [x,y]
			if (line[x] == 'U'):
				map[x][y].exitDirection = Constants.UP_DIR
			elif (line[x] == 'D'):
				map[x][y].exitDirection = Constants.DOWN_DIR
			elif (line[x] == 'L'):
				map[x][y].exitDirection = Constants.LEFT_DIR
			elif (line[x] == 'R'):
				map[x][y].exitDirection = Constants.RIGHT_DIR
			elif (line[x] == '*'):
				map[x][y].exitDirection = Constants.NO_DIR

def printMap():
	for y in range(int(sizeList[1])):
		for x in range(int(sizeList[0])):
			if map[x][y].isOccupied == True:
				print "(%s, C)" % (map[x][y].exitDirection) ,
			else:
				print "(%s,  )" % (map[x][y].exitDirection) ,
		print

def spawnCar(startLoc, endLoc, carID, direction):
	global map
	global activeCars
	map[startLoc[0]][startLoc[1]].isOccupied = True

	activeCars.append(Car(startLoc,endLoc, carID, direction))

def moveCars():
	global map
	global counter

	# Check the status of each car to see if they can move or not
	for car in activeCars:
		#print "Car %d: Start Loc: (%d,%d) Current Loc: (%d, %d), %s" % (car.carID, car.startLoc[0], car.startLoc[1], car.currentLoc[0], car.currentLoc[1], car.route)
		
		# If the car is currently in a square with exitDirection North
		if map[car.currentLoc[0]][car.currentLoc[1]].exitDirection == 1:
			# check if square to the North is empty and matches direction of the next step in route
			#print "Car %d: Checking direction North" % (car.carID)

			if map[car.currentLoc[0]][car.currentLoc[1] - 1].exitDirection == car.route[0] and map[car.currentLoc[0]][car.currentLoc[1] - 1].isOccupied == False:
				#print "Car %d: Success North" % (car.carID)
				car.nextLoc = [car.currentLoc[0],car.currentLoc[1] - 1]



		# If the car is currently in a square with exitDirection South
		elif map[car.currentLoc[0]][car.currentLoc[1]].exitDirection == 2:
			# check if square to the South is empty and matches direction of the next step in route
			#print "Car %d: Checking direction South" % (car.carID)

			if map[car.currentLoc[0]][car.currentLoc[1] + 1].exitDirection == car.route[0] and map[car.currentLoc[0]][car.currentLoc[1] + 1].isOccupied == False:
				#print "Car %d: Success South" % (car.carID)
				car.nextLoc = [car.currentLoc[0],car.currentLoc[1] + 1]



		# If the car is currently in a square with exitDirection West
		elif map[car.currentLoc[0]][car.currentLoc[1]].exitDirection == 3:
			# check if square to the West is empty and matches direction of the next step in route
			#print "Car %d: Checking direction West" % (car.carID)

			if map[car.currentLoc[0] - 1][car.currentLoc[1]].exitDirection == car.route[0] and map[car.currentLoc[0] - 1][car.currentLoc[1]].isOccupied == False:
				#print "Car %d: Success West" % (car.carID)
				car.nextLoc = [car.currentLoc[0] - 1,car.currentLoc[1]]



		# If the car is currently in a square with exitDirection East
		elif map[car.currentLoc[0]][car.currentLoc[1]].exitDirection == 4:
			# check if square to the East is empty and matches direction of the next step in route
			#print "Car %d: Checking direction East" % (car.carID)

			if map[car.currentLoc[0] + 1][car.currentLoc[1]].exitDirection == car.route[0] and map[car.currentLoc[0] + 1][car.currentLoc[1]].isOccupied == False:
				#print "Car %d: Success East" % (car.carID)
				car.nextLoc = [car.currentLoc[0] + 1,car.currentLoc[1]]

		print "Car %d: Next Move to (%d, %d)" % (car.carID, car.nextLoc[0], car.nextLoc[1])
		print

	#Update the location of all cars to their next location
	for car in reversed(activeCars):
		if car.nextLoc != car.currentLoc:
			print "Car %d Updating!" % (car.carID)
			map[car.currentLoc[0]][car.currentLoc[1]].isOccupied = False
			car.currentLoc = car.nextLoc
			del car.route[0]
			map[car.currentLoc[0]][car.currentLoc[1]].isOccupied = True
			
			if car.currentLoc == car.endLoc:
				print "Car %d reached destination! Removing from map." % (car.carID)
				map[car.currentLoc[0]][car.currentLoc[1]].isOccupied = False
				activeCars.remove(car)
		else:
			print "Car %d No Change!" %(car.carID)
		
	# Simple counter to test the movement mechanism by waiting to change the direction of (3,5) to East after 6 clocks
	counter += 1
	if counter == 6:
		map[3][5].exitDirection = 4


# Main

def main():
	# need to make main a true main
	readMap()
	printMap()

	#create car objects and add them to the map
	print "Adding Cars"
	spawnCar([2,0],[2,9], 1, [2,2,2,2,2,2,2,2,2])
	spawnCar([3,9],[5,0], 2, [1,1,1,4,4,1,1,1,1,1,1])
	spawnCar([3,8],[5,0], 3, [1,1,4,4,1,1,1,1,1,1])
	printMap()


	# 10 steps should take place, car should move each time
	while activeCars:
		moveCars()
		printMap()
		print

	print "All cars have reached their destinations"


if __name__ == "__main__": 
	main()