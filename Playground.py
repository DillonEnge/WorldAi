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

import time
import sys
import logging
import random

class World:
    def __init__(self, worldSize, goalCount, organisms):
        logging.basicConfig(filename='world.log',level=logging.DEBUG)
        logging.info("Initializing world...")
        self.organisms = organisms
        self.goalCount = goalCount
        self.goals = generateGoals(goalCount,worldSize)
        self.worldSize = worldSize
        self.generateWorldArray()
        self.generateWorldDisplay()
        self.renderCycle = 0

    def generateWorldArray(self):
        worldArray = [[0 for x in range(self.worldSize[0])] for y in range(self.worldSize[1])]

        for goal in self.goals:
            if goal.active:
                worldArray[goal.position[0]][goal.position[1]] = goal.value
        for organism in self.organisms:
            if organism.alive:
                worldArray[organism.position[0]][organism.position[1]] = organism.value

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
        for organism in self.organisms:
            if not organism.npc:
                organism.update()
        self.generateWorldArray()
        self.generateWorldDisplay()

    def beginListening(self):
        for organism in self.organisms:
            if not organism.npc:
                organism.readInput(self, self.worldSize, self.goals, self.organisms)

    def reset(self):
        logging.info('Resetting world...')
        for goal in self.goals:
            goal.active = True
        for organism in self.organisms:
            organism.position = organism.initialPosition
            organism.__init__(organism.initialPosition, organism.npc)
        self.__init__(self.worldSize, self.goalCount, self.organisms)
        self.update()

class Organism:
    def __init__(self, startingPosition, npc, hasBrain = False):
        self.initialPosition = [startingPosition[0], startingPosition[1]]
        self.position = [startingPosition[0], startingPosition[1]]
        self.actions = ["w", "a", "s", "d", "e"]
        self.brain = Brain(self)
        self.hasBrain = hasBrain
        self.npc = npc
        self.value = 4
        self.size = 20
        self.alive = True
        self.fitness = 0

    def readInput(self, world, worldSize, goals, npcs):
        key = ""
        if self.hasBrain:
            self.brain.think()
            key = self.brain.decision
        else:
            key = raw_input("Enter a key: ")

        if key == "q":
            logging.info("Quitting...")
            sys.exit()
        elif key == "r":
            world.reset()

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
                    if isTouching(self, goal) and goal.active:
                        goal.active = False
                        self.size = 20
                        logging.info("Eating... (size: " + str(self.size) + ")")

            self.fitness += 1

    def update(self):
        if self.size > 0:
            self.size -= 1
        if self.size > 7:
            self.value = 4
        elif self.size > 3:
            self.value = 3
        else:
            self.value = 1
        if self.size == 0:
            self.die()
        logging.info("Size: " + str(self.size))

    def die(self):
        self.alive = False
        self.value = 5
        print("Fitness score: " + str(self.fitness))
        key = raw_input("Continue? (y/n): ")
        if key != "y":
            logging.info("Quitting...")
            sys.exit()

class Goal:
    def __init__(self, startingPosition):
        self.position = [startingPosition[0], startingPosition[1]]
        self.active = True
        self.value = 2


def generateGoals(count, worldSize):
    goals = []
    for i in range(count):
        x = random.randint(0, worldSize[0] - 1)
        y = random.randint(0, worldSize[1] - 1)
        goals.append(Goal([x,y]))
    return goals

def generateNpcs(count, worldSize):
    x = random.randint(0, worldSize[0] - 1)
    y = random.randint(0, worldSize[1] - 1)
    npcs = [Organism([x,y], False, True)]
    for i in range(count):
        x = random.randint(0, worldSize[0] - 1)
        y = random.randint(0, worldSize[1] - 1)
        npcs.append(Organism([x,y], True))
    return npcs

def isTouching(obj1, obj2):
    for x in range(-1, 2):
            for y in range(-1, 2):
                if obj1.position == [obj2.position[0] + x, obj2.position[1] + y]:
                    return True
    return False

class Brain:
    def __init__(self, organism):
        print("Initializing...")
        self.actions = organism.actions
        organism.generation = 1
        self.decisionChain = []
    def think(self):
        print("Thinking...")
        time.sleep(2)
        self.decision = random.choice(self.actions)
        self.decisionChain.append(self.decision)



world = World([10,10], 3, generateNpcs(1, [10,10]))
while True:
    world.render()