# Car.py
# EE554 Group Project
# Spring 2017
# Car class

import Constants
from TimeObject import *

class Car(TimeObject):

	def __init__(self, startLoc, endLoc, carID, route, map):
		self.startLoc = startLoc
		self.endLoc = endLoc
		self.carID = carID
		self.route = route
		self.currentLoc = startLoc
		self.nextLoc = startLoc
		self.step = 0
		self.type = "Car"
		self.map = map

	def tick(self):
		if self.currentLoc != self.endLoc:
			self.moveCar()
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

		if self.nextLoc != self.currentLoc:
			self.map[self.currentLoc[0]][self.currentLoc[1]].isOccupied = False
			self.currentLoc = self.nextLoc
			del self.route[0]
			self.map[self.currentLoc[0]][self.currentLoc[1]].isOccupied = True

		if self.currentLoc == self.endLoc:
			return True
		else:
			return False