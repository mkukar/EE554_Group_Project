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

    def __init__(self, mapIn, startX, startY, xSizeIn, ySizeIn, ID_in):
        # default constructor
        self.map = mapIn[:][:]
        self.startIndex = [startX, startY]
        self.endIndex = [startX + (xSizeIn - 1), startY + (ySizeIn - 1)]
        self.xSize = xSizeIn
        self.ySize = ySizeIn
        self.ID = ID_in # needs a unique ID to associate it with things

        # setup will auto-size the start and end index accordingly
        self.setup()

    # #
    # Variables
    # #

    minStateTime = 2
    curStateTime = 0

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

    nextState = 0 # keeps track of next state
    nextStateJustSet = False

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
                    # should only reset the borders though, not the internal parts to prevent cars from quickly entering the intersection)
                    self.map[self.startIndex[0] - 1 + x][self.startIndex[1] - 1 + y].exitDirection = self.subMap[x][y].exitDirection
                    # actually set inside of intersection to NO_DIR for this last clock
            for y in range(self.ySize):
                for x in range(self.xSize):
                    self.map[self.startIndex[0] + x][self.startIndex[1] + y].exitDirection = [Constants.NO_DIR]

        self.yellowTimer += 1


    # takes in what squares it occupies and sets up states based on those squares
    def setup(self):

        # Sets the size of the yellow light timer
        if self.ySize > self.xSize:
            self.yellowTimerMax = self.ySize + 1
        else:
            self.yellowTimerMax = self.xSize + 1

        # ALGORITHM SUMMARY

        # Initialize all variables
        self.roads = [[Road() for y in range(self.ySize)] for x in range(self.xSize)]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # initializes roads to no direction and occupation is the same as it was previously
                self.roads[x][y].exitDirection = [Constants.NO_DIR]
                self.roads[x][y].isOccupied = self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied
                self.roads[x][y].location = self.map[x + self.startIndex[0]][y + self.startIndex[1]].location

        #print("BUG IS HERE Stoplight.py L121 - L130 probably")
        upDownState = [[Road() for y in range(self.ySize)] for x in range(self.xSize)]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # initializes roads to no direction and occupation is the same as it was previously
                upDownState[x][y].exitDirection = [Constants.NO_DIR]
                upDownState[x][y].isOccupied = self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied
                if upDownState[x][y].isOccupied:
                    print("SET SOMETHING TO UP DOWN OCCUPIED L126 Stoplight.py")
                upDownState[x][y].location = self.map[x + self.startIndex[0]][y + self.startIndex[1]].location

        leftRightState = [[Road() for y in range(self.ySize)] for x in range(self.xSize)]
        for y in range(self.ySize):
            for x in range(self.xSize):
                # initializes roads to no direction and occupation is the same as it was previously
                leftRightState[x][y].exitDirection = [Constants.NO_DIR]
                leftRightState[x][y].isOccupied = self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied
                if leftRightState[x][y].isOccupied:
                    print("SET SOMETHING TO LEFT RIGHT OCCUPIED L136 Stoplight.py")
                leftRightState[x][y].location = self.map[x + self.startIndex[0]][y + self.startIndex[1]].location

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
            #print("APPENDED UP DOWN STATE")
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
        #print("ERASE THIS LATER Stoplight.py L173 - FORCING NO VALID STATES")
        #self.states[0] = self.roads
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
        '''
        #OLD METHOD - TIMER BASED
        if (self.nextState == self.curStateIndex): # if next state is the same as the current state, just force change
            self.curStateIndex = self.curStateIndex + 1
        if self.curStateIndex >= len(self.states):
            self.curStateIndex = 0
        '''
        # just writes the next state out
        self.nextStateJustSet = False
        self.writeStateToMap(self.nextState)
        self.curStateIndex = self.nextState
        self.curStateTime = 0


    '''
    # OLD TICK METHOD
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
    '''

    # algoModeEnabled means we use the algorithm to determine enxt state, not the timer
    def tick(self, algoModeEnabled):
        self.curStateTime += 1
        if algoModeEnabled:
            
            #print("IN TICK FOR ALGO")
            if self.nextStateJustSet: # bug here - if next state is the same as current state, don't need yellow light
                if self.yellowTimer <= self.yellowTimerMax:
                    self.yellow_light()
                else:
                    self.yellowTimer = 0
                    self.changeState()
                    self.curStateIndex = self.nextState
                    #print("Got here")
            #else:
            #    self.changeState()
            #    self.curStateIndex = self.nextState
        else:
            self.timer = self.timer + 1
            if self.timer >= self.timerMax:
                if (self.yellowTimer <= self.yellowTimerMax):
                    # print("Yellow light")
                    self.yellow_light()
                else:
                    self.yellowTimer = 0
                    if self.curStateIndex + 1 >= len(self.states):
                        self.curStateIndex = 0
                        self.setNextState(self.curStateIndex)

                    else:
                        self.setNextState(self.curStateIndex + 1)
                        self.curStateIndex += 1
                    self.changeState()


    def setNextState(self, nextStateIndex):
        # CHECKS HERE TO MAKE SURE NEXT STATE IS DIFFERENT THAN CURRENT STATE
        if nextStateIndex != self.curStateIndex and self.curStateTime >= self.minStateTime:
            # note - when called it starts the yellow light timer
            self.nextState = nextStateIndex
            self.nextStateJustSet = True

    def writeStateToMap(self, stateIndex):
        # print("WRITING STATE " + str(stateIndex) + " TO MAP")
        roadsToWrite = self.states[stateIndex]
        #print("ROADS TO WRITE INFO...")
        for y in range(self.ySize):
            for x in range(self.xSize):
                #print("OCCUPIED: " + str(roadsToWrite[x][y].isOccupied))
                #print("EXIT DIRS: " + str(roadsToWrite[x][y].exitDirection))
                # first checks if the state is currently occupied to make sure it doesn't get erased
                stateOccupied = False
                if self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied:
                    stateOccupied = True
                    #print("IS OCCUPIED Stoplight.py L246")

                # now copies over the index
                self.map[x + self.startIndex[0]][y + self.startIndex[1]].exitDirection = roadsToWrite[x][y].exitDirection
                #self.map[x + self.startIndex[0]][y + self.startIndex[1]].isOccupied = stateOccupied
                #if stateOccupied:
                    #print("WROTE SOMETHING OCCUPIED Stoplight.py L249")
