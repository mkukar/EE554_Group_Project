# Algorithm.py

import time

from Road import *
import Constants

class Algorithm():

	# #
	# Constructor
	# #
	def __init__(self, timeConstraintIn):
		print("Created algorithm")
		self.timeConstraintFloat = timeConstraintIn


	# #
	# Variables
	# #

	timeConstraintFloat = 0.33

	# #
	# Functions
	# #

	# SUMMARY: Calculates the next state using our core algorithm within the time requirement set in constructor
	# ARGS: curState - current state map with cars
	# RETURNS: nextState - map of same size as curState with new directions for the map
	def calcNextState(self, curState, sizeList):
		# starts a timer from current datetime until curTime + timeConstraintFloat in seconds
		curTime = time.time()
		endTime = curTime + self.timeConstraintFloat

		loopCounter = 0 # for debug
		while(True):
			# Loops through algorithm
			# print("LOOPING!")
			loopCounter += 1

			# after the timer expires or a final result is reached, return the best next state
			if endTime <= time.time():
				print("Reached time constraint ending. Exiting (returns next state)")
				print("Loop count: " + str(loopCounter))
				return curState # currently just sends back the same state


	# SUMMARY: Most important function - calculates the heuristic by simulating the next state
	# ARGS: stateIn - map state in to calculate its heuristic value (how good is it)
	# RETURNS: heuristicVal - integer number representing our heuristic value
	# HEURISTICIN KEY:
	# 1 = use overall left/right up/down (returns [leftrighttrafficpercentage, updowntrafficpercentage])
	# 2 = use per stoplight left/right up/down (returns 2d array of above, 1 for each stop light)
	#

	def calc_heuristic(self, stateIn, sizeList, heuristicIn, timeObjects):
		res = []
		if heuristicIn == 1:
			# iterates across the state and counts how many squares that are <- or -> are occupied, then ^ down occupation)
			totalLeftRight = 0
			occupiedLeftRight = 0
			totalUpDown = 0
			occupiedUpDown = 0

			for y in range(int(sizeList[1])):
				for x in range(int(sizeList[0])):
					if Constants.DOWN_DIR in stateIn[x][y].exitDirection or Constants.UP_DIR in stateIn[x][y].exitDirection:
						totalUpDown += 1
						if stateIn[x][y].isOccupied == True:
							occupiedUpDown += 1
					elif Constants.LEFT_DIR in stateIn[x][y].exitDirection or Constants.RIGHT_DIR in stateIn[x][y].exitDirection:
						totalLeftRight += 1
						if stateIn[x][y].isOccupied == True:
							occupiedLeftRight += 1

			res = [float(occupiedLeftRight)/totalLeftRight, float(occupiedUpDown)/totalUpDown]
		elif heuristicIn == 2:
			# iterates across each of the stoplight objects and determines how many squares are occupied around them
			for obj in timeObjects:
				if obj.type == "Stoplight": # maybe change this to an int for faster execution time?
					# first looks at each stoplight object and adds its ID to our array along with its sub-heuristic
					res.append([obj.ID, self.calc_single_stoplight_heuristic(obj, stateIn, sizeList)])

			print("IN PROGRESS")
		else:
			print("INVALID HEURISTIC CODE. TRY USING 1 or 2")
		return res

	# calculates the heuristic of a single stoplight and returns it
	def calc_single_stoplight_heuristic(self, stoplightObjIn, mapIn, sizeList):
		# iterates starting at the stoplight object in each direction on the map until it hits another stoplight or
		# the end of the map
		res = [0.0,0.0,0.0,0.0] # L R U D percentage

		# ALGORITHM OVERVIEW
		# checks a side
		# if side has exit direction on same as side (e.g. constants.LEFT on LEFT side)
		# 	- iterate down until you reach the edge of map or another stoplight
		#	- count every occupied space. save value as a percentage at the end

		# TOP
		curX = 0
		curY = 0
		topTotal = 0
		topOccupied = 0
		for x in range(stoplightObjIn.xSize):
			curX = x + stoplightObjIn.startIndex[0]
			curY = stoplightObjIn.startIndex[1] - 1
			print("CHECKING INDEX " + str(curX) + "," + str(curY))
			if Constants.UP_DIR in mapIn[curX][curY].exitDirection:
				print("ITERATING UPWARDS...")
				while not mapIn[curX][curY].partOfIntersection and curY >= 0:
					print(str(curX) + ',' + str(curY))
					topTotal += 1
					if mapIn[curX][curY].isOccupied:
						topOccupied += 1
					curY -= 1

		if topTotal == 0: # prevents divide by zero errors
			res[2] = 0.0
		else:
			res[2] = float(topOccupied)/topTotal


		# BOTTOM

		bottomTotal = 0
		bottomOccupied = 0
		for x in range(stoplightObjIn.xSize):
			curX = x + stoplightObjIn.startIndex[0]
			curY = stoplightObjIn.startIndex[1] + stoplightObjIn.ySize
			print("CHECKING INDEX " + str(curX) + "," + str(curY))
			if Constants.DOWN_DIR in mapIn[curX][curY].exitDirection:
				print("ITERATING DOWNWARDS...")
				while not mapIn[curX][curY].partOfIntersection and curY < (int(sizeList[1]) - 1):
					print(str(curX) + ',' + str(curY))
					bottomTotal += 1
					if mapIn[curX][curY].isOccupied:
						bottomOccupied += 1
					curY += 1

		if bottomTotal == 0: # prevent /0
			res[3] = 0.0
		else:
			res[3] = float(bottomOccupied)/bottomTotal

		# LEFT
		leftTotal = 0
		leftOccupied = 0
		for y in range(stoplightObjIn.ySize):
			curX = stoplightObjIn.startIndex[0] - 1
			curY = y + stoplightObjIn.startIndex[1]
			print("CHECKING INDEX " + str(curX) + "," + str(curY))
			if Constants.LEFT_DIR in mapIn[curX][curY].exitDirection:
				print("ITERATING LEFTWARDS...")
				while not mapIn[curX][curY].partOfIntersection and curX >= 0:
					print(str(curX) + ',' + str(curY))
					leftTotal += 1
					if mapIn[curX][curY].isOccupied:
						leftOccupied += 1
					curX -= 1

		if leftTotal == 0:
			res[0] = 0.0
		else:
			res[0] = float(leftOccupied)/leftTotal

		# RIGHT
		rightTotal = 0
		rightOccupied = 0
		for y in range(stoplightObjIn.ySize):
			curX = stoplightObjIn.startIndex[0] + stoplightObjIn.xSize
			curY = y + stoplightObjIn.startIndex[1]
			print("CHECKING INDEX " + str(curX) + "," + str(curY))
			if Constants.LEFT_DIR in mapIn[curX][curY].exitDirection:
				print("ITERATING RIGHTWARDS...")
				while not mapIn[curX][curY].partOfIntersection and curX < (int(sizeList[0]) - 1):
					print(str(curX) + ',' + str(curY))
					rightTotal += 1
					if mapIn[curX][curY].isOccupied:
						rightOccupied += 1
					curX += 1

		if rightTotal == 0:
			res[1] = 0.0
		else:
			res[1] = float(rightOccupied)/rightTotal

		# returns [L,R,U,D] weighted
		return res


