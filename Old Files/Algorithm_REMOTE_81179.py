# Algorithm.py

import time

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
	def calcNextState(self, curState):
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
	def calc_heuristic(self, stateIn):
		print("IP")