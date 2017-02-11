
import Constants

class Road:

	# constructors
	#def __init__(self,

	def Road():
		print "this might be unncessary Road Constructor try removing with debug"

	def Road(locXIn, locYIn, dirIn):
		exitDirection = dirIn
		xLoc = locXIn
		yLoc = locYIn
		location = [xLoc, yLoc]

	def Road(locIn, dirIn):
		exitDirection = dirIn
		if (len(locIn) == 2):
			location = locIn
			xLoc = location[0]
			yLoc = location[1]
		else:
			print "You fucked up in Road.py Constructor"


	# variables
	exitDirection = Constants.NO_DIR # defaults to up
	isOccupied = False
	xLoc = -1
	yLoc = -1
	location = [xLoc, yLoc]

	# NO FUNCTIONS