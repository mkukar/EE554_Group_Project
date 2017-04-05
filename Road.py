# Road.py
# EE554 Group Project
# Spring 2017


import Constants

class Road:

	# #
	# constructors
	# #

	def Road(self):
		# print "this might be unncessary Road Constructor try removing with debug"
		pass

	def Road(self, locXIn, locYIn, dirsIn):
		exitDirection = dirsIn
		xLoc = locXIn
		yLoc = locYIn
		location = [xLoc, yLoc]

	def Road(self, locIn, dirsIn):
		exitDirection = dirsIn
		if (len(locIn) == 2):
			location = locIn
			xLoc = location[0]
			yLoc = location[1]
		else:
			print "You did something wrong up in Road.py Constructor"

	# #
	# Variables
	# #

	exitDirection = [Constants.NO_DIR] # defaults to no direction
	isOccupied = False
	xLoc = -1
	yLoc = -1
	location = [xLoc, yLoc]
	partOfIntersection = False # must be manually changed to TRUE

	# NO FUNCTIONS