# Car.py
# EE554 Group Project
# Spring 2017
# Car class

import Constants
from TimeObject import *

class Car(TimeObject):

	# original constructor with route pre-planned
	def __init__(self, startLoc, endLoc, carID, route, map):
		#if route is None:
	#		self.route = self.calculateRoute()
	#	else:
		self.route = route
		self.startLoc = startLoc
		self.endLoc = endLoc
		self.carID = carID
		self.route = route
		self.currentLoc = startLoc
		self.nextLoc = startLoc
		self.step = 0
		self.type = "Car"
		self.map = map
		self.timeAlive = 0

	def tick(self):
		if self.currentLoc != self.endLoc:
			self.moveCar()
			self.timeAlive = self.timeAlive + 1 # keeps track of how long the cars have been running alive
		else:
			print "Does something else, probably despawns car? or something"

	# checks if the intersection can be entered (there will be an empty spot on the opposite side by the time this car reaches it)
	# returns TRUE or FALSE
	def calcCanEnterIntersection(self):
		# if next road is an intersection, then we check to make sure that the empty spots on the next street is greater than the # of cars currently in the intersection
		carsInIntersection = 0
		emptySpacesInNextRoad = 0
		curIndex = 1
		if self.route[0] == Constants.UP_DIR:
			# GOING UP
			# first checks if next spot is an intersection or not
			if self.map[self.currentLoc[0]][self.currentLoc[1] - curIndex].partOfIntersection:
				# now iterates across the intersection to calculate how many cars are in the intersection
				curRoad = self.map[self.currentLoc[0]][self.currentLoc[1] - curIndex]
				while curRoad.partOfIntersection:
					curRoad = self.map[self.currentLoc[0]][self.currentLoc[1] - curIndex]
					if curRoad.isOccupied:
						carsInIntersection += 1
					curIndex += 1
				# now looks at the next roads until we hit the edge of the map or another intersection
				while (self.currentLoc[1] - curIndex) >= 0 and not curRoad.partOfIntersection:
					curRoad = self.map[self.currentLoc[0]][self.currentLoc[1] - curIndex]
					if not curRoad.isOccupied:
						emptySpacesInNextRoad += 1
					curIndex += 1
			else:
				return True # otherwise just allow the spot to continue through

		elif self.route[0] == Constants.DOWN_DIR:
			# going DOWN
			# first checks if next spot is an intersection or not
			if self.map[self.currentLoc[0]][self.currentLoc[1] + curIndex].partOfIntersection:
				# now iterates across the intersection to calculate how many cars are in the intersection
				curRoad = self.map[self.currentLoc[0]][self.currentLoc[1] + curIndex]
				while curRoad.partOfIntersection:
					curRoad = self.map[self.currentLoc[0]][self.currentLoc[1] + curIndex]
					if curRoad.isOccupied:
						carsInIntersection += 1
					curIndex += 1
				# now looks at the next roads until we hit the edge of the map or another intersection
				while (self.currentLoc[1] + curIndex) < len(self.map[:]) and not curRoad.partOfIntersection:
					curRoad = self.map[self.currentLoc[0]][self.currentLoc[1] + curIndex]
					if not curRoad.isOccupied:
						emptySpacesInNextRoad += 1
					curIndex += 1
			else:
				return True # otherwise just allow the spot to continue through

		elif self.route[0] == Constants.LEFT_DIR:
			# going LEFT
			# first checks if next spot is an intersection or not
			if self.map[self.currentLoc[0] - curIndex][self.currentLoc[1]].partOfIntersection:
				# now iterates across the intersection to calculate how many cars are in the intersection
				curRoad = self.map[self.currentLoc[0] - curIndex][self.currentLoc[1]]
				while curRoad.partOfIntersection:
					curRoad = self.map[self.currentLoc[0] - curIndex][self.currentLoc[1]]
					if curRoad.isOccupied:
						carsInIntersection += 1
					curIndex += 1
				# now looks at the next roads until we hit the edge of the map or another intersection
				while (self.currentLoc[0] - curIndex) >= 0 and not curRoad.partOfIntersection:
					curRoad = self.map[self.currentLoc[0] - curIndex][self.currentLoc[1]]
					if not curRoad.isOccupied:
						emptySpacesInNextRoad += 1
					curIndex += 1
			else:
				return True # otherwise just allow the spot to continue through
		elif self.route[0] == Constants.RIGHT_DIR:
			# going RIGHT
			# first checks if next spot is an intersection or not
			if self.map[self.currentLoc[0] + curIndex][self.currentLoc[1]].partOfIntersection:
				# now iterates across the intersection to calculate how many cars are in the intersection
				curRoad = self.map[self.currentLoc[0] + curIndex][self.currentLoc[1]]
				while curRoad.partOfIntersection:
					curRoad = self.map[self.currentLoc[0] + curIndex][self.currentLoc[1]]
					if curRoad.isOccupied:
						carsInIntersection += 1
					curIndex += 1
				# now looks at the next roads until we hit the edge of the map or another intersection
				while (self.currentLoc[0] + curIndex) < len(self.map) and not curRoad.partOfIntersection:
					curRoad = self.map[self.currentLoc[0] + curIndex][self.currentLoc[1]]
					if not curRoad.isOccupied:
						emptySpacesInNextRoad += 1
					curIndex += 1
			else:
				return True # otherwise just allow the spot to continue through

		if emptySpacesInNextRoad > carsInIntersection: # must be greater so we have at least 1 space for our car
			return True
		else:
			return False


	def setNextLocation(self):

		# allows cars to exit intersections no matter what
		if self.map[self.currentLoc[0]][self.currentLoc[1]].partOfIntersection:
			if self.route[0] == Constants.UP_DIR:
				if self.map[self.currentLoc[0]][self.currentLoc[1] - 1].isOccupied == False:
					self.nextLoc = [self.currentLoc[0], self.currentLoc[1] - 1]
			elif self.route[0] == Constants.DOWN_DIR:
				if self.map[self.currentLoc[0]][self.currentLoc[1] + 1].isOccupied == False:
					self.nextLoc = [self.currentLoc[0], self.currentLoc[1] + 1]
			elif self.route[0] == Constants.RIGHT_DIR:
				if self.map[self.currentLoc[0]+1][self.currentLoc[1]].isOccupied == False:
					self.nextLoc = [self.currentLoc[0]+1, self.currentLoc[1]]
			elif self.route[0] == Constants.LEFT_DIR:
				if self.map[self.currentLoc[0]-1][self.currentLoc[1]].isOccupied == False:
					self.nextLoc = [self.currentLoc[0]-1, self.currentLoc[1]]

		# normal movement
		if Constants.UP_DIR in self.map[self.currentLoc[0]][self.currentLoc[1]].exitDirection:
			if self.route[0] in self.map[self.currentLoc[0]][self.currentLoc[1] - 1].exitDirection and self.map[self.currentLoc[0]][self.currentLoc[1] - 1].isOccupied == False and self.calcCanEnterIntersection():
				self.nextLoc = [self.currentLoc[0],self.currentLoc[1] - 1]

		elif Constants.DOWN_DIR in self.map[self.currentLoc[0]][self.currentLoc[1]].exitDirection:
			if self.route[0] in self.map[self.currentLoc[0]][self.currentLoc[1] + 1].exitDirection and self.map[self.currentLoc[0]][self.currentLoc[1] + 1].isOccupied == False and self.calcCanEnterIntersection():
				self.nextLoc = [self.currentLoc[0],self.currentLoc[1] + 1]

		elif Constants.LEFT_DIR in self.map[self.currentLoc[0]][self.currentLoc[1]].exitDirection:
			if self.route[0] in self.map[self.currentLoc[0] - 1][self.currentLoc[1]].exitDirection and self.map[self.currentLoc[0] - 1][self.currentLoc[1]].isOccupied == False and self.calcCanEnterIntersection():
				self.nextLoc = [self.currentLoc[0] - 1, self.currentLoc[1]]

		elif Constants.RIGHT_DIR in self.map[self.currentLoc[0]][self.currentLoc[1]].exitDirection:
			if self.route[0] in self.map[self.currentLoc[0] + 1][self.currentLoc[1]].exitDirection and self.map[self.currentLoc[0] + 1][self.currentLoc[1]].isOccupied == False and self.calcCanEnterIntersection():
				self.nextLoc = [self.currentLoc[0] + 1, self.currentLoc[1]]


	# returns True when car reaches its final destination
	def moveCar(self):
		self.timeAlive = self.timeAlive + 1
		if self.nextLoc != self.currentLoc:

			self.map[self.currentLoc[0]][self.currentLoc[1]].isOccupied = False
			self.currentLoc = self.nextLoc
			del self.route[0]
			self.map[self.currentLoc[0]][self.currentLoc[1]].isOccupied = True
			#print("SETTING LOCATION OCCUPIED Car.py L63")
			#print("Coordinates are: " + str(self.currentLoc[0]) + "," + str(self.currentLoc[1]))

		if self.currentLoc == self.endLoc:
			return True
		else:
			return False

	# Calculates the route using the internal start and end points, along with the map itself
	def calculateRoute(self):
		print("ROUTE PLANNING IN PROGRESS - DO NOT USE")