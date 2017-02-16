# Car.py
# EE554 Group Project
# Spring 2017
# Car class

import Constants
from TimeObject import *

class Car(TimeObject):

	def __init__(self, startLoc, endLoc, carID, route):
		self.startLoc = startLoc
		self.endLoc = endLoc
		self.carID = carID
		self.route = route
		self.currentLoc = startLoc
		self.nextLoc = startLoc
		self.step = 0

	def tick(self):
		if self.currentLoc != self.endLoc:
			self.moveCar()
		else:
			print "Does something else, probably despawns car? or something"

	def moveCar(self):
		print "MOVECAR() IN PROGRESS"