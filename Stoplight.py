# Stoplight.py
# EE554 Group Project
# Spring 2017
# Controls the stoplights

from Road import *
from TimeObject import *
import Constants

# TO DO
# - handle any edge cases (or design map around them)
# - add right turn functionality (add to each state initialization)
# - add left turn functionality
#   - update map to prevent entrance of side roads during intersection (similar strategy as yellow light)

class Stoplight(TimeObject):

    # #
    # Constructors
    # #

    def __init__(self, mapIn, startX, startY, xSizeIn, ySizeIn):
        # default constructor
        self.map = mapIn[:][:]
        self.startIndex = [startX, startY]
        self.endIndex = [startX + (xSizeIn - 1), startY + (ySizeIn - 1)]
        self.xSize = xSizeIn
        self.ySize = ySizeIn

        # setup will auto-size the start and end index accordingly
        print("SETTING UP STOPLIGHT")
        self.setup()
        print("STOPLIGHT SETUP COMPLETE")

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
    timerMax = 6
    yellowTimer = 0
    yellowTimerMax = 2 # should scale to the max length of the longest road itself
    type = "Stoplight"
    subMap = [[]]

    # #
    # Functions
    # #

    # allows for yellow lights to prevent erasing cars (blocks cars from entering intersection)
    def yellow_light(self):

        if self.yellowTimer == 0:
            # print("INITIALIZING YELLOW LIGHT")
            # sets all the intersection entry points to not allow any cars into the intersections
            # still will allow exit directions (e.g. > > > > will become * > > > to allow cars only to leave

            # saves current map state (aligned to -1,-1 of intersection

            self.subMap = [[Road() for y in range(self.ySize + 2)] for x in range(self.xSize + 2)]
            for y in range(self.ySize + 2):
                for x in range(self.xSize + 2):
                    self.subMap[x][y].exitDirection = self.map[self.startIndex[0] - 1 + x][self.startIndex[1] - 1 + y].exitDirection

            # now overwrites initial map with a map with no entries into the intersection
            for x in range(self.xSize):
                # DOWN IS ENTRANCE
                if Constants.DOWN_DIR in self.map[self.startIndex[0] + x][self.startIndex[1] - 1].exitDirection:
                    self.map[self.startIndex[0] + x][self.startIndex[1] - 1].exitDirection = [Constants.NO_DIR]

                # UP IS ENTRANCE
                if Constants.UP_DIR in self.map[self.startIndex[0] + x][self.startIndex[1] + self.ySize].exitDirection:
                    self.map[self.startIndex[0] + x][self.startIndex[1] + self.ySize].exitDirection = [Constants.NO_DIR]

            for y in range(self.ySize):
                # RIGHT IS ENTRANCE
                if Constants.RIGHT_DIR in self.map[self.startIndex[0] - 1][self.startIndex[1] + y].exitDirection:
                    self.map[self.startIndex[0] - 1][self.startIndex[1] + y].exitDirection = [Constants.NO_DIR]

                # LEFT IS ENTRANCE
                if Constants.LEFT_DIR in self.map[self.startIndex[0] + self.xSize][self.startIndex[1] + y].exitDirection:
                    self.map[self.startIndex[0] + self.xSize][self.startIndex[1] + y].exitDirection = [Constants.NO_DIR]

        elif self.yellowTimer >= self.yellowTimerMax:
            # print("RESETTING YELLOW TIMER")
            # goes back to self.subMap
            for y in range(self.ySize + 2):
                for x in range(self.xSize + 2):
                    self.map[self.startIndex[0] - 1 + x][self.startIndex[1] - 1 + y].exitDirection = self.subMap[x][y].exitDirection

        self.yellowTimer += 1


    # takes in what squares it occupies and sets up states based on those squares
    def setup(self):

        # Sets the size of the yellow light timer
        if self.ySize > self.xSize:
            self.yellowTimerMax = self.ySize
        else:
            self.yellowTimerMax = self.xSize

        # ALGORITHM SUMMARY

        # Initialize all variables
        self.roads = [[Road() for y in range(self.ySize)] for x in range(self.xSize)]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # initializes roads to no direction and occupation is the same as it was previously
                self.roads[x][y].exitDirection = [Constants.NO_DIR]
                self.roads[x][y].isOccupied = self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied
                self.roads[x][y].location = self.map[x + self.startIndex[0]][y + self.startIndex[1]]

        upDownState = [[Road() for y in range(self.ySize)] for x in range(self.xSize)]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # initializes roads to no direction and occupation is the same as it was previously
                upDownState[x][y].exitDirection = [Constants.NO_DIR]
                upDownState[x][y].isOccupied = self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied
                if upDownState[x][y].isOccupied:
                    print("SET SOMETHING TO UP DOWN OCCUPIED L126 Stoplight.py")
                upDownState[x][y].location = self.map[x + self.startIndex[0]][y + self.startIndex[1]]

        leftRightState = [[Road() for y in range(self.ySize)] for x in range(self.xSize)]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # initializes roads to no direction and occupation is the same as it was previously
                leftRightState[x][y].exitDirection = [Constants.NO_DIR]
                leftRightState[x][y].isOccupied = self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied
                if leftRightState[x][y].isOccupied:
                    print("SET SOMETHING TO LEFT RIGHT OCCUPIED L136 Stoplight.py")
                leftRightState[x][y].location = self.map[x + self.startIndex[0]][y + self.startIndex[1]]

        # Now determine each state individually (up/down state, then left/right state)

        # UP DOWN STATE DETECTION
        validState = False
        for column in range(self.xSize):
            if self.map[column + self.startIndex[0]][self.startIndex[1] - 1].exitDirection == \
                    self.map[column + self.startIndex[0]][self.startIndex[1] + self.ySize].exitDirection:
                if Constants.DOWN_DIR in self.map[column + self.startIndex[0]][self.startIndex[1] - 1].exitDirection   or \
                    Constants.UP_DIR in self.map[column + self.startIndex[0]][self.startIndex[1] - 1].exitDirection:
                    validState = True
                    for yIndex in range(self.ySize):
                        upDownState[column][yIndex].exitDirection = self.map[column + self.startIndex[0]][self.startIndex[1]-1].exitDirection
        if validState:
            self.states.append(upDownState)


        # RIGHT LEFT STATE DETECTION
        validState = False
        for row in range(self.ySize):
            # checks left and right index equal, and it is a L or R
            if self.map[self.startIndex[0] - 1][self.startIndex[1] + row].exitDirection == \
                    self.map[self.startIndex[0] + self.xSize][self.startIndex[1] + row].exitDirection:
                if Constants.LEFT_DIR in self.map[self.startIndex[0] - 1][self.startIndex[1] + row].exitDirection or \
                    Constants.RIGHT_DIR in self.map[self.startIndex[0] - 1][self.startIndex[1] + row].exitDirection:
                    validState = True
                    for xIndex in range(self.xSize):
                        leftRightState[xIndex][row].exitDirection = self.map[self.startIndex[0] - 1][self.startIndex[1] + row].exitDirection
        if validState:
            self.states.append(leftRightState)


        # Now setup the first state and write it to the map
        if len(self.states) == 0:
            print("NO VALID STATES, INTERSECTION WILL BE TURNED OFF")
            self.states.append(self.roads)
        self.roads = self.states[self.curStateIndex]
        self.writeStateToMap(self.curStateIndex)

        '''
        # TEST CODE, ERASE LATER
        # creates a singlular index with two states just for fun
        # relies on "stoplight_map_test.txt"
        #self.xSize = 1
        #self.ySize = 1
        self.endIndex = self.startIndex
        self.roads = [[Road() for y in range(self.ySize)] for x in range(self.xSize)]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # initializes roads to no direction and occupation is the same as it was previously
                self.roads[x][y].exitDirection = [Constants.NO_DIR]
                self.roads[x][y].isOccupied = self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied

        state1 = [[Road() for y in range(self.ySize)] for x in range(self.xSize)]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # initializes roads to no direction and occupation is the same as it was previously
                state1[x][y].exitDirection = [Constants.UP_DIR]
                state1[x][y].isOccupied = self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied

        state2 = [[Road() for y in range(self.ySize)] for x in range(self.xSize)]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # initializes roads to no direction and occupation is the same as it was previously
                state2[x][y].exitDirection = [Constants.RIGHT_DIR]
                state2[x][y].isOccupied = self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied

        self.states.append(state1)
        self.states.append(state2)

        self.roads = self.states[self.curStateIndex]
        self.writeStateToMap(self.curStateIndex)
        '''

    def changeState(self):
        # print("CHANGING STATE...")
        self.curStateIndex = self.curStateIndex + 1
        if self.curStateIndex >= len(self.states):
            self.curStateIndex = 0

        self.writeStateToMap(self.curStateIndex)


    def tick(self):
        self.timer = self.timer + 1
        if self.timer >= self.timerMax:
            # first goes into yellow light state (ticks inside there until completion)
            if(self.yellowTimer <= self.yellowTimerMax):
                # print("YELLOW LIGHT")
                self.yellow_light()
            else:
                self.yellowTimer = 0 # resets timer
                # now changes state and starts the next one
                self.changeState()
                self.timer = 0


    def writeStateToMap(self, stateIndex):
        # print("WRITING STATE " + str(stateIndex) + " TO MAP")
        roadsToWrite = self.states[stateIndex]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # first checks if the state is currently occupied to make sure it doesn't get erased
                stateOccupied = False
                if self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied:
                    stateOccupied = True
                    print("IS OCCUPIED Stoplight.py L246")

                # now copies over the index
                self.map[x + self.startIndex[0]][y + self.startIndex[1]] = roadsToWrite[x][y]
                self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied = stateOccupied
                if stateOccupied:
                    print("WROTE SOMETHING OCCUPIED Stoplight.py L249")
