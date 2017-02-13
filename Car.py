# Car.py
# EE554 Group Project
# Spring 2017
# Car class

import Constants


class Car(object):

	def __init__(self, startLoc, endLoc, carID, route):
		self.startLoc = startLoc
		self.endLoc = endLoc
		self.carID = carID
		self.route = route
		self.currentLoc = startLoc
		self.nextLoc = startLoc
		self.step = 0

    def moveCar():
        print "IN PROGRESS"