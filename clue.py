# The CLUE Bookkeeper
# Keeps your detective notes for the board game Clue 

#Author: Dawn Pattison
#Date: 12/12/2014

#Keeps two types of information
#1) Your notepad. {Player 1: Conservatory: 'X', Knife: 'O', 'Miss Scarlet': 'U'}
#Player 1 doesn't have conservatory, has the knife, and unknown if carrying Miss Scarlet

#2) You potentials.  Say I'm Player 1.  Player 3 disproves Player 2's guess.
#Now, I didn't get to see the card, but I know player 3 has one of three cards.
#These cards are logged in potentials.


#=============================================================

#Game cards:
suspects = ['Colonel Mustard', 'Miss Scarlet', 'Mr. Green', 'Mrs. Peacock', 'Mrs. White', 'Professor Plum']

weapons = ['Candlestick', 'Knife', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench']

rooms = ['Ballroom', 'Billiard Room', 'Conservatory', 'Dining Room', 'Hall', 'Kitchen', 'Library', 'Lounge', 'Study']
#Function prints correct spellings
def correctSpellings():
            print " "
            print "==================================================="
            print "Unknown spelling. Please reference list below."
            print " "
            print "SUSPECTS: %s" %", ".join(suspects)
            print " "
            print "ROOMS: %s" %", ".join(rooms)
            print " "
            print "WEAPONS: %s" %", ".join(weapons)
            print " "
            print "==================================================="
            
#=============================================================

#Number of players function, outputs integer
def numberPlayers():
    numPlayers = int(raw_input("Enter number of players (3-6): "))
    return numPlayers

#=============================================================

#Tells computer which player is you
#Outputs list with one string element, your name
def yourName():
    print " "
    you = [raw_input("What is your name? ")]
    return you

#=============================================================

#Asks for names of remaining players in clockwise fashion.
#Outputs list of all players 
def playerOrder():
    playerList = you[:] #You are included in the list of players!
    for i in range (0, (numPlayers)-1):
        j = raw_input("Enter next player, clockwise: ")
        playerList.append(j)
    return playerList


def otherPlayers():
    others = playerList[:]
    others.remove("".join(you))
    return others
#=============================================================

#Dictionary generator (will be part of your detective notepad)
dictionary = {}
for i in suspects:

    dictionary[i]="U"
for i in weapons:
    dictionary[i] = "U"
for i in rooms:
    dictionary[i]= "U"

#Returns potential dictionary
def playerToEmpty():
    potential = {key:[] for key in playerList}
    return potential

#Returns notepad (dictionary of dictionaries)
def notepadGenerator():
    notepad = potential.copy()
    for key in notepad.keys():
        notepad[key]=dictionary.copy()
    return notepad
#============================================================= 

#Updates information based on your cards

#Returns integer
def numberCards():
    numCards = int(raw_input ("How many cards do you have? "))
    return numCards
    
#Updates notepad with your cards.
def yourCards():
    yours = "".join(you)
    for i in notepad[yours].keys():
        notepad[yours][i] = 'X'

    print ""
    
    card = 0
    while card < numCards:
        j = raw_input("Enter card: ")
        if j in notepad[yours].keys():
            notepad[yours][j] = 'O'
            card+=1
            for k in range(len(others)):
                notepad[others[k]][j]='X'                  
        else:
            correctSpellings()
            
#=============================================================
#List of functions for guessing:

def whoseTurn():
    counters = 0
    while counters < 1:
        print " "
        start = raw_input("Who is guessing? ")
        if start not in playerList:
            print "I do not recognize this player."
        else:
            counters +=1
    return start

def whichSuspect():
    counters = 0
    while counters <1:
        suspect = raw_input ("It was (suspect): ")
        if suspect not in suspects:
             correctSpellings()
        else:
             counters += 1
    return suspect

def whichRoom():
    counters = 0
    while counters <1:
        room = raw_input ("... in the (room) : ")
        if room not in rooms:
             correctSpellings()
        else:
             counters += 1
    return room

def whichWeapon():
    counters = 0
    while counters <1:
        weapon = raw_input ("...with a (weapon) : ")
        if weapon not in weapons:
             correctSpellings()
        else:
             counters += 1
    counters = 0
    return weapon

def whoDisproved():
    counters = 0
    while counters < 1:
        stop = raw_input("Who disproved? ")
        if stop not in playerList:
            print "I do not recognize this player."
        else:
            counters +=1
    return stop

#============================================================
#Function for inputting cards guessed, and cards revealed.

def guess():

    start = whoseTurn()
    suspect = whichSuspect()
    room = whichRoom()
    weapon = whichWeapon()
    stop = whoDisproved()

    i = (playerList.index(start)+1)% numPlayers
    j = playerList.index(stop)
    threeCards = [suspect, room, weapon]

    #Every player between the one who guessed and the one who
    #disproved does not have any of the cards
    while i!= j:
        notepad[playerList[i]][suspect] = 'X'
        notepad[playerList[i]][room] = 'X'
        notepad[playerList[i]][weapon] = 'X'
        i = (i+1)% numPlayers

    #As long as you don't disprove yourself:
    if stop != "".join(you):
        #If you're the one guessing, you learn a new card
        if start == "".join(you):  
            counter = 0
            while counter < 1:        
                known = raw_input ("Which card were you shown? ")
                if known in dictionary.keys():
                    counter+=1
                else:
                    correctSpellings()
            deduced = [[known, stop]]       
            while deduced != []:
                for pair in deduced:
                    updateNotepad(pair[0], pair[1])
                deduced = checkAll()
        #If you're not the one guessing, you know the person who
        #disproved has at least one of the three cards
        else:
            potential[stop].append([suspect, room, weapon])
            deduced = [['dummy', 'dummy']]
            tick=0
            while deduced != []:
                if tick != 0:
                    for pair in deduced:
                        updateNotepad(pair[0], pair[1])
                deduced = checkAll()
                tick=1
                  
#=============================================================
#Functions to update notepad and potential as guesses are made.
#Functions are called inside guess function, above

#update notepad
def updateNotepad(known, stop):
    notepad[stop][known] = 'O'
    temp = playerList[:]
    temp.remove(stop)

    for i in range(len(temp)):
        notepad[temp[i]][known] = 'X'

#Function checks every card in notepad against potential list
#Where all deductions are made!  For example, If Player 1 guesses 3 cards,  and
#Player 2 disproves and I've seen 2 of the 3, I know which card
#Player 2 is holding
        
def checkAll():
    for player in playerList:
        removeElement = []
        removeLine = []
        for line in range(len(potential[player])):
            for element in potential[player][line]:
                if notepad[player][element] == 'X':
                    removeElement.append(element)
                elif notepad[player][element] == 'O':
                    removeLine.append(potential[player][line])
                    
        for i in removeElement:
            for line in range(len(potential[player])):
                if i in potential[player][line]:
                    potential[player][line].remove(i)
        for j in removeLine:
            if j in potential[player]:
                potential[player].remove(j)
           
    for player in playerList:
        deduced = []
           
        for p in playerList:
            for i in range(len(potential[p])):
                    if len(potential[p][i]) == 1:
                            deduced.append([potential[p][i][0], p])
        print deduced
        return deduced
#=============================================================
#Formats notepad printing

def notepadPrint():

    heading = playerList[:]
    heading.insert(0, 'Cards')
    data = []
    
    for suspect in suspects:
        strings = []
        for player in playerList:
            strings.append(notepad[player][suspect])
            if len(strings) == numPlayers:
                strings.insert(0, suspect)
                data.append(strings)
    data.append([])
                
              
    for room in rooms:
        strings = []
        for player in playerList:
            strings.append(notepad[player][room])
            if len(strings) == numPlayers:
                strings.insert(0, room)
                data.append(strings)
    data.append([])
    for weapon in weapons:
        strings = []
        for player in playerList:
            strings.append(notepad[player][weapon])
            if len(strings) == numPlayers:
                strings.insert(0, weapon)
                data.append(strings)

    
    data.insert(0, heading)
    col_width = max(len(word) for row in data for word in row) + 2
    for row in data:
        print "".join(word.ljust(col_width) for word in row)
        

#=============================================================
#Formats potential printing

def potentialPrint():
    for other in others:
        for trio in potential[other]:
            print other+" has:" + " "+ " or ".join(trio)

#=============================================================
#Main game function:
def play():
    accusedSuspect = "unknown"
    accusedRoom = "unknown"
    accusedWeapon = "unknown"
    
                   
    while accusedSuspect =="unknown" or accusedRoom == "unknown" or accusedWeapon =="unknown":
        guess()
        for suspect in suspects:
            suspecttemp = 0
            for player in playerList:
                if notepad[player][suspect] == 'X':
                    suspecttemp+=1
                    if suspecttemp == 3:
                        accusedSuspect = suspect
        for room in rooms:
            roomtemp = 0
            for player in playerList:
                if notepad[player][room] == 'X':
                    roomtemp+=1
                    if roomtemp == 3:
                        accusedRoom = room
        for weapon in weapons:
            weapontemp = 0
            for player in playerList:
                if notepad[player][weapon] == 'X':
                    weapontemp+=1
                    if weapontemp == 3:
                        accusedWeapon = weapon
        print  "==================================================="
        print "Deduced suspect: ", accusedSuspect
        print "Deduced room: ", accusedRoom
        print "Deduced weapon: ", accusedWeapon
        print ""
        
        notepadPrint()
        print ""
        potentialPrint()

 #"==================================================="
 #GAME STARTS HERE 
            
numPlayers = numberPlayers()
you = yourName()
playerList = playerOrder()
others = otherPlayers()
potential = playerToEmpty()
notepad = notepadGenerator()
numCards = numberCards()
yourCards()
notepadPrint()
play()






    
