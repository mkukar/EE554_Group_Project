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

    def Stoplight(self, mapIn, cordsIn):
        # default constructor
        self.map = mapIn
        self.coordinates = cordsIn
        self.setup()


    # allows for the timer to be altered globally
    def Stoplight(self, mapIn, cordsIn, maxTimer):
        self.map = mapIn
        self.coordinates = cordsIn
        self.timerMax = maxTimer
        self.setup()


    # #
    # Variables
    # #

    coordinates = {} # dictionary mapping x to y coordinates for the roads we can effect
    roads = []
    states = [] # array of different states of the roads in different configurations
    timer = 0
    timerMax = 30


    # #
    # Functions
    # #


    # takes in what squares it occupies and sets up states based on those squares
    def setup(self):
        print "IP"


    def changeState(self):
        print "IP"


    def tick(self):
        self.timer = self.timer + 1
        if self.timer >= self.timerMax:
            self.changeState()
            self.timer = 0