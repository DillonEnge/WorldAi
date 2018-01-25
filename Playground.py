# Goals: survival, physical maintenance, hoarding, dominance, preening and mating.
# Variable Goals: items, respect, children.
# Actions: move, mate, clean oneself, fight, collect
# Emotions: love, hate, fear, lust, and contentment.
# World: 
# | - - - - - - - - - - - |
# | - - - - - - - - - - - |
# | - - - o - - - - - - - |
# | - - - - - - - - - - - |
# | - - - - - - - - - - - |
# | - - - - - - - x - - - |
# | - - - - - - - - - - - |
# | - - - - - - - - - - - |
# | - - - - - - - - - - - |
# | - - - - - - - - - - - |

import sys
import logging
from random import *

class World:
    def __init__(self, worldSize, goalCount, organism):
        logging.basicConfig(filename='world.log',level=logging.DEBUG)
        logging.info("Initializing world...")
        self.organism = organism
        self.goalCount = goalCount
        self.goals = generateGoals(goalCount,[10,10])
        self.worldSize = worldSize
        self.generateWorldArray()
        self.generateWorldDisplay()
        self.renderCycle = 0

    def generateWorldArray(self):
        worldArray = [[0 for x in range(self.worldSize[0])] for y in range(self.worldSize[1])]
        for goal in self.goals:
            if goal.active:
                worldArray[goal.position[0]][goal.position[1]] = goal.value
        worldArray[self.organism.position[0]][self.organism.position[1]] = self.organism.value

        self.worldArray = worldArray

    def generateWorldDisplay(self):
        worldDisplay = ""

        for x in self.worldArray:
            worldDisplay += "|"
            for y in x:
                if y == 1:
                    worldDisplay += " o"
                elif y == 2:
                    worldDisplay += " x"
                elif y == 3:
                    worldDisplay += " O"
                elif y == 4:
                    worldDisplay += " 0"
                elif y == 5:
                    worldDisplay += " T"
                else:
                    worldDisplay += " -"
            worldDisplay += " |\n"

        worldDisplay = worldDisplay[:worldDisplay.rfind("\n")]

        self.worldDisplay = worldDisplay

    def render(self):
        self.update()
        print(self.worldDisplay)
        self.renderCycle += 1
        self.beginListening()

    def update(self):
        logging.info("Updating world...")
        self.organism.update()
        self.generateWorldArray()
        self.generateWorldDisplay()

    def beginListening(self):
        key = raw_input("Enter a key: ")
        if key == "q":
            logging.info("Quitting...")
            sys.exit()
        if key == "r":
            self.reset()
        self.organism.readInput(key, self.worldSize, self.goals)

    def reset(self):
        logging.info('Resetting world...')
        self.organism.position = self.organism.initialPosition
        for goal in self.goals:
            goal.active = True
        self.organism.__init__(self.organism.initialPosition)
        self.__init__(self.worldSize, self.goalCount, self.organism)
        self.update()

class Organism:
    def __init__(self, startingPosition):
        self.initialPosition = [startingPosition[0], startingPosition[1]]
        self.position = [startingPosition[0], startingPosition[1]]
        self.hunger = 0
        self.value = 4
        self.size = 20
        self.alive = True

    def readInput(self, key, worldSize, goals):
        if self.alive:
            if key == "w" and self.position[0] > 0:
                self.position[0] -= 1
                logging.info("Moving...")
            elif key == "a" and self.position[1] > 0:
                self.position[1] -= 1
                logging.info("Moving...")
            elif key == "s" and self.position[0] < worldSize[0] - 1:
                self.position[0] += 1
                logging.info("Moving...")
            elif key == "d" and self.position[1] < worldSize[1] - 1:
                self.position[1] += 1
                logging.info("Moving...")
            elif key == "e":
                for goal in goals:
                    if self.position == goal.position and goal.active:
                        goal.active = False
                        self.hunger = 0
                        self.size = 20
                        logging.info("Eating... (size: " + str(self.size) + ")")

    def update(self):
        if self.hunger < 20:
            self.hunger += 1

        if self.size > 0:
            self.size -= 1
        if self.size > 7:
            self.value = 4
        elif self.size > 3:
            self.value = 3
        else:
            self.value = 1
        if self.hunger == 20:
            self.die()
        logging.info("Hunger: " + str(self.hunger))
        logging.info("Size: " + str(self.size))

    def die(self):
        self.alive = False
        self.value = 5

class Goal:
    def __init__(self, startingPosition):
        self.position = [startingPosition[0], startingPosition[1]]
        self.active = True
        self.value = 2


def generateGoals(count, worldSize):
    goals = []
    for x in range(count):
        x = randint(0, worldSize[0] - 1)
        y = randint(0, worldSize[1] - 1)
        goals.append(Goal([x,y]))
    return goals

class BrainStage1:
    def __init__(self):
        print("Initializing")

world = World([10,10], 3, Organism([4,0]))
while True:
    world.render()
