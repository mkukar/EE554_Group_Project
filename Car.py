# Car

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