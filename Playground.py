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

class World:
    def __init__(self, worldSize, goal, organism):
        logging.basicConfig(filename='world.log',level=logging.DEBUG)
        logging.info("Initializing world...")
        self.organism = organism
        self.goal = goal
        self.worldSize = worldSize
        self.generateWorldArray()
        self.generateWorldDisplay()
        self.renderCycle = 0

    def generateWorldArray(self):
        worldArray = [[0 for x in range(self.worldSize[0])] for y in range(self.worldSize[1])]
        if self.goal.active:
            worldArray[self.goal.position[0]][self.goal.position[1]] = self.goal.value
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
        self.organism.readInput(key, self.worldSize, self.goal)

    def reset(self):
        logging.info('Resetting world...')

class Organism:
    def __init__(self, startingPosition):
        self.position = [startingPosition[0], startingPosition[1]]
        self.value = 1
        self.size = 1
    def readInput(self, key, worldSize, goal):
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
        elif key == "e" and self.position == goal.position and goal.active:
            goal.active = False
            self.size += 1
            logging.info("Eating... (size: " + str(self.size) + ")")
    def update(self):
        if self.size > 1:
            self.value = 3

class Goal:
    def __init__(self, startingPosition):
        self.position = [startingPosition[0], startingPosition[1]]
        self.active = True
        self.value = 2

class BrainStage1:
    def __init__(self):
        print("Initializing")

world = World([10,10], Goal([0,4]), Organism([4,0]))
while True:
    world.render()
