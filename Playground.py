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
import csv

PLAYABLE = False

class World:
    def __init__(self, worldSize, goalCount, organisms):
        logging.basicConfig(filename='world.log',level=logging.DEBUG)
        logging.info("Initializing world...")
        self.organisms = organisms
        self.goalCount = goalCount
        self.goals = generateGoals(goalCount,worldSize,organisms)
        self.worldSize = worldSize
        self.generateWorldArray()
        self.generateWorldDisplay()
        self.renderCycle = 0

    def generateWorldArray(self):
        worldArray = [[0 for x in range(self.worldSize[1])] for y in range(self.worldSize[0])]

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
        for goal in self.goals:
            if goal.active == False:
                self.goals.remove(goal)
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
    ACTIONS = ["w", "a", "s", "d", "e"]
    def __init__(self, startingPosition, npc, brain = None):
        self.initialPosition = [startingPosition[0], startingPosition[1]]
        self.position = [startingPosition[0], startingPosition[1]]
        self.direction = "left"
        self.brain = brain
        self.npc = npc
        self.value = 4
        self.size = 20
        self.alive = True
        self.fitness = 0
        self.eatingPath = []

    def readInput(self, world, worldSize, goals, npcs):
        key = ""
        if self.brain:
            self.visibleGoalAction(goals)
            self.brain.think()
            key = self.brain.decision
        else:
            key = raw_input("Enter a key: ")

        if key == "q":
            logging.info("Quitting...")
            sys.exit()
        elif key == "r":
            world.reset()

        if len(self.eatingPath) > 0:
            key = self.eatingPath[0]
            del self.eatingPath[0]

        canMove = self.canMove(goals)

        if self.alive:
            if key == "w" and self.position[0] > 0 and canMove[0]:
                self.position[0] -= 1
                self.direction = "up"
                logging.info("Moving...")
            elif key == "a" and self.position[1] > 0 and canMove[1]:
                self.position[1] -= 1
                self.direction = "left"
                logging.info("Moving...")
            elif key == "s" and self.position[0] < worldSize[0] - 1 and canMove[2]:
                self.position[0] += 1
                self.direction = "down"
                logging.info("Moving...")
            elif key == "d" and self.position[1] < worldSize[1] - 1 and canMove[3]:
                self.position[1] += 1
                self.direction = "right"
                logging.info("Moving...")
            elif key == "e":
                for goal in goals:
                    if isTouching(self, goal) and goal.active:
                        goal.active = False
                        self.size = 20
                        logging.info("Eating... (size: " + str(self.size) + ")")
                        break
            elif key[0] == "go" and len(key) > 1:
                print("FOOOOOOOD!!!") #Temporary so I could see when he was going for the food
                self.findFastestPath(key)
                
            if self.brain:
                self.brain.fitness += 1

    def canSeeGoal(self, goal):
        if self.direction == "left":
            if goal.position[1] <= self.position[1]:
                return True
        elif self.direction == "up":
            if goal.position[0] <= self.position[0]:
                return True
        elif self.direction == "right":
            if goal.position[1] >= self.position[1]:
                return True
        elif self.direction == "down":
            if goal.position[0] >= self.position[0]:
                return True
        return False

    def visibleGoalAction(self, goals):
        for action in self.brain.actions:
            if action[0] == "go":
                self.brain.actions.remove(action)
        visibleGoals = ["go"]
        for goal in goals:
            if self.canSeeGoal(goal):
                visibleGoals.append([goal.position[0],goal.position[1]])
        if len(visibleGoals) >= 2:
            self.brain.actions.append(visibleGoals)

    def findFastestPath(self, key):
        path = []
        lowestPathSize = 1000
        pathSize =0
        for goal in key:
                if goal != "go":
                    yChange = goal[0] - self.position[0]
                    xChange = goal[1] - self.position[1]
                    pathSize = abs(xChange) + abs(yChange)
                    if pathSize < lowestPathSize:
                        lowestPathSize = pathSize
                        lowestX = xChange
                        lowestY = yChange
        for i in range(lowestPathSize):
            if lowestX > 0:
                path.append("d")
                lowestX -= 1
            if lowestY > 0:
                path.append("s")
                lowestY -= 1
            if lowestX < 0:
                path.append("a")
                lowestX += 1
            if lowestY < 0:
                path.append("w")
                lowestY += 1
        del path[lowestPathSize-1]
        path.append("e")
        self.eatingPath = path

    def canMove(self, goals):
        canMove = [True, True, True, True]
        for goal in goals:
            if goal.position[0] == (self.position[0] - 1):
                if goal.position[1] == self.position[1]:
                    canMove[0] = False
            if goal.position[1] == (self.position[1] - 1):
                if goal.position[0] == self.position[0]:
                    canMove[1] = False
            if goal.position[0] == (self.position[0] + 1):
                if goal.position[1] == self.position[1]:
                    canMove[2] = False
            if goal.position[1] == (self.position[1] + 1):
                if goal.position[0] == self.position[0]:
                    canMove[3] = False
        return canMove
                    

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
        if self.brain:
            print("Fitness score: " + str(self.brain.fitness))
            self.brain.uploadDataToHiveMind(self)
        key = raw_input("Continue? (y/n): ")
        if key != "y":
            logging.info("Quitting...")
            sys.exit()

class Goal:
    def __init__(self, startingPosition):
        self.position = [startingPosition[0], startingPosition[1]]
        self.active = True
        self.value = 2


def generateGoals(count, worldSize, organisms):
    goals = []
    for i in range(count):
        spotNotTaken = True
        x = random.randint(0, worldSize[0] - 1)
        y = random.randint(0, worldSize[1] - 1)
        for organism in organisms:
            if x == organism.position[1] and y == organism.position[0]:
                spotNotTaken = False
        if spotNotTaken:
            goals.append(Goal([x,y]))
        else:
            i -= 1
    return goals

def generateNpcs(count, worldSize):
    x = random.randint(0, worldSize[0] - 1)
    y = random.randint(0, worldSize[1] - 1)
    npcs = []

    if PLAYABLE:
        npcs = [Organism([x,y], False)]
    else:
        npcs = [Organism([x,y], False, Brain())]

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
    def __init__(self):
        print("Initializing...")
        self.actions = Organism.ACTIONS
        self.fitness = 1
        self.decisionChain = []
    def think(self):
        print("Thinking...")
        time.sleep(2)
        self.decision = random.choice(self.actions)
        self.decisionChain.append(self.decision)
    def uploadDataToHiveMind(self, organism):
        hiveMind.writeData([str(self.fitness), str(self.decisionChain)])
    def getDataFromHiveMind(self):
        hiveMind.accessData()

class HiveMind:
    def __init__(self):
        self.data = open("BrainData.csv", "w+")
    def accessData(self):
        processedData = csv.reader(self.data, delimiter=",")
        return processedData
    def writeData(self, row):
        csvWriter = csv.writer(self.data, delimiter=",")
        csvWriter.writerow(row)

hiveMind = HiveMind()
world = World([10,20], 2, generateNpcs(0, [10,20]))
while True:
    world.render()