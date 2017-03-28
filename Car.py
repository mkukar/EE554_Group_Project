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

	def setNextLocation(self):

		if Constants.UP_DIR in self.map[self.currentLoc[0]][self.currentLoc[1]].exitDirection:
			if self.route[0] in self.map[self.currentLoc[0]][self.currentLoc[1] - 1].exitDirection and self.map[self.currentLoc[0]][self.currentLoc[1] - 1].isOccupied == False:
				self.nextLoc = [self.currentLoc[0],self.currentLoc[1] - 1]

		elif Constants.DOWN_DIR in self.map[self.currentLoc[0]][self.currentLoc[1]].exitDirection:
			if self.route[0] in self.map[self.currentLoc[0]][self.currentLoc[1] + 1].exitDirection and self.map[self.currentLoc[0]][self.currentLoc[1] + 1].isOccupied == False:
				self.nextLoc = [self.currentLoc[0],self.currentLoc[1] + 1]

		elif Constants.LEFT_DIR in self.map[self.currentLoc[0]][self.currentLoc[1]].exitDirection:
			if self.route[0] in self.map[self.currentLoc[0] - 1][self.currentLoc[1]].exitDirection and self.map[self.currentLoc[0] - 1][self.currentLoc[1]].isOccupied == False:
				self.nextLoc = [self.currentLoc[0] - 1, self.currentLoc[1]]

		elif Constants.RIGHT_DIR in self.map[self.currentLoc[0]][self.currentLoc[1]].exitDirection:
			if self.route[0] in self.map[self.currentLoc[0] + 1][self.currentLoc[1]].exitDirection and self.map[self.currentLoc[0] + 1][self.currentLoc[1]].isOccupied == False:
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