import random
import time
import main

#add target and sender objects ?
def moveDecoder(moveToTranslate):
    moveCharList = []
    for x in moveToTranslate:
      moveCharList.append(x)

    match moveCharList[0]:
      case 'a':
        numberOfRolls = int(moveCharList[1])
        rollOutOf = int(moveCharList[2] + moveCharList[3])
        baseDamage = int(moveCharList[5] + moveCharList[6])
        return ['a', executeAttack(numberOfRolls, rollOutOf, baseDamage)]
      case 's':
        return ['s', 0]
      case 'g':
         return ['g', (random.randint(0, 4))]
      case 'm':
        return ['m', 0]
      case 'n':
        return ['n', 0]

#fire, water, earth, air, normal
def calclulateTypeAdvantage(attackingType, defendingType):
  if attackingType in defendingType:
    pass

def executeAttack(numOfRolls, rollNum, baseDmg):
  damageTotal = baseDmg
  for x in range(0, numOfRolls):
    damageTotal += random.randint(0, rollNum)
  return damageTotal

class Enemy():

  name = ''
  type = 0
  enemyhealth = 0
  enemyCurrentHealth = 0
  enemyguardHealth = 0
  enemyStrength = 0
  enemyInitiative = 0
  enemyConstitution = 0
  enemyIntelligence = 0 
  moveset = []
  movesetPatterns = []
  currentPattern = []
  currentMoveWithinPattern = 0
  nextMove = []

  def makeMove(self):

      #Move to the next move in the sequence. If you have finished the sequence, roll a new random one.
      moveMade = moveDecoder(self.moveset[int(self.currentPattern[self.currentMoveWithinPattern])-1])

      self.currentMoveWithinPattern += 1
      if self.currentMoveWithinPattern + 1 > len(self.currentPattern):
        self.currentMoveWithinPattern = 0
        self.currentPattern = self.movesetPatterns[random.randint(0, len(self.movesetPatterns) - 1)]
      #Decode the chosen move and store it.
      self.nextMove = moveDecoder(self.moveset[int(self.currentPattern[self.currentMoveWithinPattern])-1])

      try:
        match moveMade[0]:
          case 'a':
            time.sleep(.5)
            print('The ' + self.name + ' attacks for ' + str(round(moveMade[1])) + ' points of damage!')
            return moveMade
          case 'g':
            time.sleep(.5)
            return ['g', 0]
          case 's':
            return ['s', 0]
          case 'n':
            return ['n', 0]
          case 'm':
            return ['m', 0]
      except TypeError:
        return ['n', 0]
      
  def applyPlayerMove(self, moveInfo):
    moveAmp = 0
    try:
      if self.nextMove[0] == 'g':
        self.enemyguardHealth = self.nextMove[1] + (2 * self.enemyConstitution)
    except IndexError:
      self.nextMove = self.moveset[int(self.currentPattern[self.currentMoveWithinPattern])-1]
      if self.nextMove[0] == 'g':
        self.enemyguardHealth = self.nextMove[1] + (2 * self.enemyConstitution)
    match moveInfo[0]:
      case 'a':
        moveAmp = moveInfo[1]
        if self.enemyguardHealth >= moveAmp:
          time.sleep(.25)
          print('But it was blocked fully!')
          self.enemyguardHealth = 0
          moveAmp = 0
        if self.enemyguardHealth > 0:
          print('The ' + self.name + ' guarded against your attack!')
          moveAmp -= self.enemyguardHealth
        damageTaken = round(moveAmp * (1 - (self.enemyConstitution * 0.025)))
        time.sleep(.5)
        print('The ' + self.name +' takes ' + str(damageTaken) + ' damage.')
        self.enemyCurrentHealth -= damageTaken

  def loadEnemyData(self):

    #Store all data points within a list for later reference
    enemyAttrbList = []
    with open('gameTextAssets.txt', 'r'):
      for x in pullFromTextAssets('ID:  ' + str(self.type)):
        enemyAttrbList.append(x.strip('\n'))

      #Set all easy attributes like stats and health and name
      self.enemyStrength = int(enemyAttrbList[0][-2:])
      self.enemyInitiative = int(enemyAttrbList[1][-2:])
      self.enemyConstitution = int(enemyAttrbList[2][-2:])
      self.enemyIntelligence = int(enemyAttrbList[3][-2:])
      self.enemyhealth = int(enemyAttrbList[4][-3:])

      #Run through all move codes
      for x in range(1, int(enemyAttrbList[5][-2:]) + 1):
        self.moveset.append(enemyAttrbList[5 + x])


      #Find out how many move patterns there are, and list and store them appropriately.
      lineAfterMoves = 6 + len(self.moveset)
      rawList = []
      for x in range (0, int(enemyAttrbList[lineAfterMoves][-2:])):
        for move in enemyAttrbList[x + lineAfterMoves + 1]:
          if (move != ','):
            rawList.append(move)
        self.movesetPatterns.append(rawList)
        rawList = []
      
      self.name = enemyAttrbList[-1]
      self.enemyCurrentHealth = self.enemyhealth
      self.currentMoveWithinPattern = 0
      self.currentPattern = self.movesetPatterns[random.randint(0, len(self.movesetPatterns) - 1)]

  #Upon creation of this entity, define name and type.
  def __init__(self, name, type):
    self.name = name
    self.type = type
    self.moveset = []
class Area:
  name = ""
  number = 0

  cFEnemy = 0
  cFEnvironment = 0
  cFMerchant = 0
  cFNPC = 0
  cFDevilsWheel = 0
  cFHazard = 0
  cFChoice = 0
  cFShrine = 0
  cFBoss = 0
  chanceDistribution = []
  possibleEnemies = []

  def rollRandomEncounter(self):
    encounter = random.randint(0, 99)
    returnList = ['n', 0]
    match self.chanceDistribution[encounter]:
      case 1:
        returnList = self.loadCombatEncounter()
    return returnList
        
  def loadCombatEncounter(self):
    returnList = ['c']
    enemyRolled = random.randint(1, len(self.possibleEnemies))
    returnList.append(enemyRolled)
    return returnList
  
  def loadAreaFromFile(self, areaNumber):
    areaAttrbList = []
    for x in pullFromTextAssets('Area ' + str(areaNumber)):
      areaAttrbList.append(x[-4:])

    self.cFEnemy = areaAttrbList[0]
    self.cFEnvironment = areaAttrbList[1]
    self.cFMerchant = areaAttrbList[2]
    self.cFNPC = areaAttrbList[3]
    self.cFDevilsWheel = areaAttrbList[4]
    self.cFHazard = areaAttrbList[5]
    self.cFChoice = areaAttrbList[6]
    self.cFShrine = areaAttrbList[7]
    self.cFBoss = areaAttrbList[8]

    for currentEncter, eventChance in enumerate(areaAttrbList):
      for x in range(0, int(eventChance)):
        self.chanceDistribution.append(int(currentEncter) + 1)

    for x in range (0, int(areaAttrbList[9][-4:])):
      self.possibleEnemies.append(int(areaAttrbList[10 + x].strip('\n')))


  def __init__(self, name, number):
    self.name = name
    self.number = number
def printFromTextAssets(neededLine):
  for x in pullFromTextAssets(neededLine):
    print(x.strip('\n'))
def pullFromTextAssets(neededLine):

  #A MESS.
  firstLineToPull = ""
  lastLineToPull = ""
  returnList = []
  with open("gameTextAssets.txt") as file:

    #Run through file and find title needed, then pull the specified exerpt of text that comes after.
    for num, line in enumerate(file):
      if neededLine in line:
        linesToPull = line[-4:].strip("\n").strip(" ")
        firstLineToPull = num + 1
        lastLineToPull = num + int(linesToPull)
        
      #If the title has been found and the first and last lines have been found, pull the text from the file and add it to the return list.
      if firstLineToPull != "" and lastLineToPull != "":
        if num >= int(firstLineToPull) and num < int(lastLineToPull):
          returnList.append(line)
        elif num == int(lastLineToPull):
          returnList.append(line)
          break

  #Return the list that we created.
  return returnList
def searchForItemInFile(itemToSearchFor, fileToSearchIn):

  #Search file for a specific item, and store all lines of those items and return them.
  with open(fileToSearchIn, 'r') as file:
    instances = []
    for line in file.readlines():
      if itemToSearchFor in line:
        instances.append(line)
      else:
        pass
  return instances