# Stoplight.py
# EE554 Group Project
# Spring 2017
# Controls the stoplights

from Road import *
from TimeObject import *
import Constants

class Stoplight(TimeObject):

    # #
    # Constructors
    # #

    def __init__(self, mapIn, startX, startY):
        # default constructor
        self.map = mapIn
        self.startIndex = [startX, startY]
        self.endIndex = [startX, startY]
        self.xSize = 1
        self.ySize = 1

        # setup will auto-size the start and end index accordingly
        self.setup()

    # #
    # Variables
    # #

    startIndex = [-1,-1] # x,y coordinates of the upper left corner (starting index)
    endIndex = [-1,-1] # x,y coordinates of the lower right corner (ending index, inclusive)
    xSize = -1 # absolute size (e.g. 1 is just 1 index wide, 2 is two index wide, etc.)
    ySize = -1
    roads = [[]] # 2D array (list of lists) which stores the roads to write into the map at any given state
    curStateIndex = 0
    states = [] # array of different states of the roads in different configurations, one for each state
    timer = 0
    timerMax = 5
    type = "Stoplight"

    # #
    # Functions
    # #


    # takes in what squares it occupies and sets up states based on those squares
    def setup(self):
        print "IP IN STOPLIGHT SETUP"

        # TEST CODE, ERASE LATER
        # creates a singlular index with two states just for fun
        # relies on "stoplight_map_test.txt"
        self.xSize = 1
        self.ySize = 1
        self.endIndex = self.startIndex
        self.roads = [[Road() for x in range(self.xSize)] for y in range(self.ySize)]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # initializes roads to no direction and occupation is the same as it was previously
                self.roads[x][y].exitDirection = [Constants.NO_DIR]
                self.roads[x][y].isOccupied = self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied

        state1 = [[Road() for x in range(self.xSize)] for y in range(self.ySize)]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # initializes roads to no direction and occupation is the same as it was previously
                state1[x][y].exitDirection = [Constants.UP_DIR]
                state1[x][y].isOccupied = self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied

        state2 = [[Road() for x in range(self.xSize)] for y in range(self.ySize)]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # initializes roads to no direction and occupation is the same as it was previously
                state2[x][y].exitDirection = [Constants.RIGHT_DIR]
                state2[x][y].isOccupied = self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied

        self.states.append(state1)
        self.states.append(state2)

        self.roads = self.states[self.curStateIndex]
        self.writeStateToMap(self.curStateIndex)


    def changeState(self):
        print("CHANGING STATE...")
        self.curStateIndex = self.curStateIndex + 1
        if self.curStateIndex >= len(self.states):
            self.curStateIndex = 0

        self.writeStateToMap(self.curStateIndex)


    def tick(self):
        self.timer = self.timer + 1
        if self.timer >= self.timerMax:
            self.changeState()
            self.timer = 0


    def writeStateToMap(self, stateIndex):
        print("WRITING STATE " + str(stateIndex) + " TO MAP")
        roadsToWrite = self.states[stateIndex]
        for y in range(self.ySize):
            for x in range(self.xSize):
                self.map[x + self.startIndex[0]][y + self.startIndex[1]] = roadsToWrite[x][y]
