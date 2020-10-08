import json
import random as r



class Tile:
    def __init__(self, char, ptval):
        #Letter
        self.char = char

        #Point value 
        self.ptval = ptval

        #Adjacent tiles (up, down, left, right)
        self.adj = [None, None, None, None]
    def __str__(self):
        return f"[{self.char}{self.ptval}] "

class User:
    def __init__(self, name):
        self.name = name
        self.letters = []
        self.MAXCT = 7

        self.choices = {
                "s": {
                        "text": "Shuffle Letters", 
                        "fn": self.shuffleLetters,
                        "endTurn": False
                    },
                "v": {
                        "text": "View Rack", 
                        "fn": self.printRack,
                        "endTurn": False
                    }

                }
     

    def getChoice(self):
        while True:
            for key in self.choices.keys():
                print(f"{key}: {self.choices[key]['text']}")
            choice = input("Enter your choice -> ")
            if choice in self.choices.keys():
                break
        return self.choices[choice]

    def _condenseletters(self):
        self.letters = [item for item in self.letters if item]

    def getRackStr(self):
        retStr = ""
        for tile in self.letters:
            retStr += f"{tile!s}"
        return retStr 

    def printRack(self):
        print(self.getRackStr())

    def drawLetters(self,pool,num=0):

        if num > pool.getSize():
            self.letters.extend(pool.getNLetters(pool.getSize())) 
            return False

        #If user specifies number, draw that many
        if num:
            self.letters.extend(pool.getNLetters(num)) 
            return True
        #If num=0, draw enough to fill rack 
        else:
            self.letters.extend(pool.getNLetters(self.MAXCT - len(self.letters))) 
            return True

    def showLetters(self):
        for l in self.letters:
            print(l)

    def shuffleLetters(self):
        r.shuffle(self.letters)

    def takeTurn(self):
        print(f"{self.name}'s turn")
        while True:
            choice = self.getChoice() 
            choice['fn']()
            if choice['endTurn']:
                break
            else:
                print(f"Still {self.name}'s turn")


class LetterPool:
    def __init__(self):
        self.initfile = "tiles.json"
        with open(self.initfile, "r") as f:
            letterDict = json.load(f)
        self.pool = []
        for key in letterDict.keys():
            self.pool.extend([Tile(key,letterDict[key]['ptVal']) for i in range(letterDict[key]['numTiles'])])
    def getSize(self):
        return len(self.pool)
    def getNLetters(self, n):
        if self.getSize() == 0:
            return None
        if self.getSize() < n:
            n = self.getSize()
        #TODO GET TILES
        retList = []
        for _ in range(n):
            retList.append(self.pool.pop(r.randint(0,len(self.pool)-1)))
        return retList

class Board:
    def __init__(self):
        self.SIZE = 15





class Game:
    def __init__(self, numPlayers=2):
        #Initialize letter pool
        self.letters = LetterPool()

        self.players = []
        #TODO make more flexible
        self.players.append(User("P1"))
        self.players.append(User("P2"))


        for p in self.players:
            p.drawLetters(self.letters)


    def playGame(self):
        lastTurn = False
        while not lastTurn:
            for player in self.players:
                player.takeTurn()
            if self.letters.getSize == 0:
                lastTurn = True


