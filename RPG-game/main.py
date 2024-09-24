import math
import os
import random
import time
import methodDump as mD

menuLine = '--------------------------------------------------------------'
affirmitive = ["yes", "y"]
negative = ["no", "n"]
validActions = ['guard', 'attack', 'm1', 'm2', 'm3', 'm4', 'wait']

def printBattleUI(enemyObject):
  tempStringVar1 = ''
  tempStringVar2 = ''

  print(menuLine)
  print('PLAYER:                \\    /  _______              ' + enemyEncountered.name + ':')

  tempStringVar1 = str(player.currentHealth) + '/' + str(player.maxHealth) + ' HP'
  tempStringVar2 = str(enemyEncountered.enemyCurrentHealth) + '/' + str(enemyEncountered.enemyhealth) + ' HP'
  print(tempStringVar1 + '                \\  /  |______             ' + tempStringVar2)
  tempStringVar1 = str(player.currentMana) + '/' + str(player.maxMana) + ' MP'
  tempStringVar2 = str(0) + '/' + str(0) + ' MP'
  print(tempStringVar1 + '                 \\/.   ______|.           ' + tempStringVar2)
  print(menuLine)
  print('[attack]: Physical Attack                [guard]: Put up guard \n[stat]: View character info              [info]: Examine enemy\n[spell]: View known spells               [wait]: Skip one turn\n[item]: View usable items                [log]: View enemy log')

#Player specific variables, if is to condense
if (True):
  playerName = ""
  playerStrength = 0
  playerInitiative = 0
  playerConstitution = 0
  playerIntelligence = 0
  playerLevel = 0
  playerExperience = 0
  playerHealth = 0
  playerMana = 0
  #Hand 1, Hand 2, Armor, Trinkets 1-3
  playerEquipment = [0, 0, 0, 0, 0, 0]
  playerLearnedSpells = [0, 0, 0, 0]
  playerInventory = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  playerArea = 0

class playerEntity():

  strength = 0
  initiative = 0
  constitution = 0
  intelligence = 0
  maxHealth = 0
  currentHealth = 0
  guardHealth = 0
  currentMana = 0
  maxMana = 0
  
  def takeAction(self, enemyAppliedTo):
    actionTaken = ''
    while actionTaken not in validActions:
      printBattleUI(enemyAppliedTo)
      actionTaken = input('Your move: ')
    os.system('cls')
    match actionTaken:
      case 'attack':
        damageDealt = (1 + (playerConstitution * 0.025)) * self.rollPlayerAttack(6, 2, 4)
        print('You swing for ' + str(damageDealt) + ' damage.')
        enemyEncountered.applyPlayerMove(['a', damageDealt])
      case 'guard':
        print('You defend as best you can.')
        player.guardHealth += 2 * player.constitution + random.randint(0, 4)

  def rollPlayerAttack(self, baseDmg, numOfRolls, rollNum):
    damageTotal = baseDmg
    for x in range(0, numOfRolls):
      damageTotal += random.randint(0, rollNum)
    return damageTotal

  def applyEnemyMove(self, moveGiven):
    if moveGiven[0] != 'n':
      moveType = moveGiven[0]
      moveAmp = 0
      match moveType:
        case 'a':
          moveAmp = moveGiven[1]
          if self.guardHealth >= moveAmp:
            time.sleep(.3)
            print('But you blocked it fully!')
            self.guardHealth = 0
            moveAmp = 0
          else:
            moveAmp -= self.guardHealth
          time.sleep(.3)
          print('You take ' + str(round(moveAmp * (1 - (playerConstitution * 0.025)))) + ' damage.')
          self.currentHealth -= round(moveAmp * (1 - (playerConstitution * 0.025)))
          self.guardHealth = 0
        case 'g':
          pass


  def __init__(self):
    self.strength = playerStrength
    self.initiative = playerInitiative
    self.constitution = playerConstitution
    self.intelligence = playerIntelligence
    self.maxHealth = playerHealth
    self.currentHealth = playerHealth
    self.maxMana = playerMana
    self.currentMana = self.maxMana

#While a character is not yet loaded:
charLoaded = False
while not charLoaded:

  def characterCreation():

    #Loop until the user is happy with character
    done = ""
    newCharacterInfo = []
    characterPool = ["Warrior", "Mage", "Rogue"]
    characterStatPool = [[5, 3, 4, 3], [2, 4, 2, 6], [3, 6, 3, 4]]

    while done not in affirmitive:
      os.system("cls")
      newCharacterInfo = []

      #Get the character's name
      print("What is your first party member's name?")
      newCharacterInfo.append(input("Name: "))
      os.system('cls')

      #Character selection screen
      characterChoice = '?'

      #Screen loops until valid character choice is entered
      while characterChoice != "1" and characterChoice != "2" and characterChoice != "3":
        mD.printFromTextAssets('Character Select Screen')
        characterChoice = input("")

        #If the user enters a question mark, show the stat inforomation
        if characterChoice == "?":
          os.system('cls')
          mD.printFromTextAssets("Stat Information")
          input("\n\nEnter to continue.")
        os.system('cls')

        #If the user enters a number, add the character to the new character info
        if characterChoice == "1" or characterChoice == "2" or characterChoice == "3":
          newCharacterInfo.append(int(characterChoice))

      #Verify that all information is correct
      print("Is this information correct?")
      print((newCharacterInfo[0]) + " the " +
            (characterPool[int(newCharacterInfo[1]) - 1]))
      done = (input("Y/N: ")).lower()

    #When done with information gathering, create character in file
    os.system('cls')
    print("Creating character...")
    with open("characterinfo.txt", 'a') as file:

      #Add all character information to the file in order
      file.write("!" + newCharacterInfo[0] + " the " +
                 characterPool[int(newCharacterInfo[1]) - 1] + "\n")

      #Writing Stats
      charStatList = characterStatPool[int(newCharacterInfo[1]) - 1]
      for x in charStatList:
        file.write(str(x) + "\n")

      #Level and Experience
      file.write("-\n")
      file.write('1\n0\n')

      #Vitals (Health and Mana)
      file.write("-\n")
      file.write(str(int(charStatList[2]) * 3 + 20) + '\n')
      file.write(str(int(charStatList[3]) * 8 + 20) + '\n')

      #Class specific equipment (coming later once IDs work)
      file.write("-\n")
      file.write('0\n0\n0\n0\n0\n0\n')

      #Spells known, also class specific (coming later once spell IDs work)
      file.write("-\n")
      file.write('0\n0\n0\n0\n')

      #Inventory creation
      file.write("-\n")
      for x in range(0, 10):
        file.write("0\n")

      #Area of the character
      file.write("-\n")
      file.write("0\n")

    print('Character created! Returning to home screen.')
  def loadCharacterFile():

    global playerName
    global playerStrength
    global playerInitiative
    global playerConstitution
    global playerIntelligence 
    global playerLevel
    global playerExperience
    global playerHealth
    global playerMana
    #Hand 1, Hand 2, Armor, Trinkets 1-3
    global playerEquipment
    global playerLearnedSpells
    global playerInventory
    global playerArea

    #Load character file and apply information to appropriate variables (will encrypt before release)
    infoToAdd = []
    with open("characterinfo.txt", 'r') as charInfo:
      for line in charInfo:
        if line.strip('\n') != '-':
          infoToAdd.append(line.strip('\n'))

    #Add information to appropriate variables
    playerName = infoToAdd[0].strip("!\n")
    playerStrength = int(infoToAdd[1])
    playerInitiative = int(infoToAdd[2])
    playerConstitution = int(infoToAdd[3])
    playerIntelligence = int(infoToAdd[4])
    playerLevel = int(infoToAdd[5])
    playerExperience = int(infoToAdd[6])
    playerHealth = int(infoToAdd[7])
    playerMana = int(infoToAdd[8])
    for num in range(0, 6):
      playerEquipment[num] = int(infoToAdd[9 + num])
    for num in range(0, 4):
      playerLearnedSpells[num] = int(infoToAdd[15 + num])
    for num in range(0, 10):
      playerInventory[num] = int(infoToAdd[19 + num])
    playerArea = int(infoToAdd[29])

    print("Character loaded!")

  #Game Start
  print("Welcome to the SigmaSlicer.")

  #Check if needed game files are present. If not, force quit.
  try:
    with open("gameTextAssets.txt"):
      pass
  except FileNotFoundError:
    print(
        "Files critical to the function of this game are missing. Please redownload or fix the issue."
    )
    time.sleep(7)
    exit()

  #Check if the player has a save file. If not, create one.
  try:
    with open("characterinfo.txt", "r"):
      pass
  except FileNotFoundError:
    #No character files found, creating a new file
    print("You do not have a character. Would you like to create one?")
    create = (input("Y/N: ")).lower()
    if create in affirmitive:
      characterCreation()
    elif create in negative:
      print("Quitting game.")
      exit()
  os.system('cls')

  #If the player has a character, ask if they want to load it. Loop until either quit or character loaded.
  #If there is a character info file but no character, or incompete info, reset it.
  if len(mD.searchForItemInFile('!', 'characterinfo.txt')) == 0:
    print(
        "Either your character is corrupted, or there is some error on our end. Delete stored information?"
    )
    delete = (input("Y/N: ")).lower()

    #If the user wants to delete the character info, delete it. Otherwise, close.
    if delete in affirmitive:
      os.remove("characterinfo.txt")
      print("Character deleted. Restarting program.")
      time.sleep(1.5)
      exit()
    elif delete in negative:
      print("Quitting game.")
      time.sleep(1.5)
      exit()

  #If a character exists in the file, ask if they want to load it. Otherwise, create new
  else:
    with open("characterinfo.txt", "r") as charInfo:
      print("Welcome adventurer! I remember you as being: " +
            str(charInfo.readlines(1)[0]).strip('!'))
      print(
          "Use this character? (Y/N), N will delete the character and begin a new character creation."
      )
      create = (input('')).lower()

      #Old file is decided not to be used, delete and create new
      if create in negative:
        charInfo.close()
        os.remove("characterinfo.txt")
        print("Character deleted. Creating new character.")
        time.sleep(1.5)
        characterCreation()

      #With player consent, load selected character file.
      elif create in affirmitive:
        print("Loading character...")
        loadCharacterFile()
        charLoaded = True

#Entering Gameplay Loop
currentArea = mD.Area("Meadows", 1)
currentArea.loadAreaFromFile(1)
activelyPlaying = True
print('Welcome to the SigmaSlicer! You are in area one. Press enter to begin your journey.')
input('')
os.system('cls')
player = playerEntity()
while activelyPlaying:
    currentEncounter = currentArea.rollRandomEncounter()
    inEncounter = True

    #Determine what kind of encounter it is and handle it properly
    match currentEncounter[0]:

      #If the event is a combat event, load the enemy you face and begin the encounter
      case 'c':
        enemyEncountered = mD.Enemy('', currentEncounter[1])
        enemyEncountered.loadEnemyData()
        print('You have encountered a ' + enemyEncountered.name + '!')
        time.sleep(.5)
        #Until one combatant is dead, loop through the turn based combat.
        while inEncounter:
          player.takeAction(enemyEncountered)
          if enemyEncountered.enemyCurrentHealth <= 0:
            inEncounter = False
            break
          if inEncounter:
            time.sleep(.3)
            player.applyEnemyMove(enemyEncountered.makeMove())
            player.guardHealth = 0
          if player.currentHealth <= 0:
            activelyPlaying = False
            inEncounter = False
          time.sleep(.5)
          input('Enter to continue. ')
          os.system('cls')
        time.sleep(.75)
        print(enemyEncountered.name + ' defeated!')
        del(enemyEncountered)
        time.sleep(1)
        input('\nYou ready yourself, then continue your journey.')
        os.system('cls')
print('L you lost')