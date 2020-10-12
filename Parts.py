import json
import random as r
import copy



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
    def __repr__(self):
        return f"{self.char}"
    def __eq__(self, other):
        if isinstance(other, str):
            return self.char == other
        elif isinstance(other, Tile):
            return self.char == other.char
        else:
            return False 

class Player:
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
                    },
                "p": {
                    "text": "Play a word", 
                    "fn": self.playWord,
                    "endTurn": True
                    }

                }



        def getChoice(self):
            while True:
                for key in self.choices.keys():
                    print(f"{key}: {self.choices[key]['text']}")
                choice = input("What would you like to do? Enter your choice -> ")
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

    def getRackLetters(self):
        return [t.char for t in self.letters]

    def searchRack(self,char):
        char = char.upper()
        if char!= " " and char not in self.getRackLetters():
            return None
        else:
            for idx, tile in enumerate(self.letters):
                if tile.char == char:
                    ret = self.letters.pop(idx)
                    self._condenseletters()
                    return ret


    def printRack(self):
        print(self.getRackStr())

    def playWord(self,*args):
        #If word is passed to function, use that word
        if not args:
            pass

        #If no args passed, use input method
        while True:
            word = list(input("Enter the letters to be used ->").upper())
            toPlay = []

            for letter in word:
                tile=self.searchRack(letter)
                if tile:
                    toPlay.append(tile)
                else:
                    print("Sorry, {letter} is not in your rack.")
                    continue

            print(f"Letters chosen: {''.join([t.char for t in toPlay])}")
            print(f"letters remaining in rack: {[t.char for t in self.letters]}")

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

    def takeTurn(self, *args):
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

class Square:
    def __init__(self, multNum=1, multType=None):
        self.tile = None
        self.letter = ""
        self.multNum = multNum
        self.multType = multType

        self.pending = False

    def placeTile(self, tile):
        if self.tile:
            return False
        else:
            self.tile = tile
            self.letter = tile.char
            return True



class Board:
    def __init__(self):
        self.SIZE = 15
        self.MAX = self.SIZE - 1 
        self.board = [[Square() for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.center = self.board[8][8]

    def placeTile(self, tile, x,y):
        if self.board[x][y].tile is None:
            self.board[x][y].placeTile(tile)
            return True
        else:
            print(f"Tile is already laid at {x}, {y}")
            return False

    def placeWord(self, word, direction, x,y):
        '''
       word: list of TILE OBJECTS to be played (in order)
       direction: 'a', 'd' (across or down)
       x: x location of word start
       y: y location of word start
       '''

        #Make a backup of the board in case user tries to break it
        origBoard = copy.deepcopy(self.board)
    
        #Check that word will not go off edge of board 
        if direction == 'a' and (len(word)+x) > self.MAX:
            return False
        if direction == 'd' and (len(word)+y) > self.MAX:
            return False

        #Word fits on boundaries of board.
        #Now check if the tiles are clear

        #Horizontal Code
        if direction == 'a':
            for i, tile in enumerate(word):
                result = self.placeTile(tile,x+i,y)
                if result is False:
                    #TODO GET RID OF TILES
                    self.board = origBoard
                    return False
        #Vertical code
        if direction == 'd':
            for i, tile in enumerate(word):
                result = self.placeTile(tile,x,y+i)
                if result is False:
                    #TODO GET RID OF TILES
                    self.board = origBoard
                    return False
        
        return True

    def printBoard(self):
        print("   ", end="")
        for idx in range(self.SIZE):
            print("{0: >2}".format(idx), end="")
        print()
        for idx in range(self.SIZE):
            print("{0: <2} |".format(idx), end="")
            for jdx in range(self.SIZE):
                sq = self.board[idx][jdx]
                if sq.tile == None:
                    print(" ", end="|")
                elif sq.letter == " ":
                    print("*", end="|")
                else:
                    print(f"{sq.letter}", end="|")
            #Print new line
            print("") 

class Game:
    def __init__(self, numPlayers=2):


        self.board = Board()

        #Initialize letter pool
        self.letters = LetterPool()

        self.players = []
        #TODO make more flexible
        for i in range(numPlayers):
            player = Player(f"P{i}") 
            self.players.append(player)

        for p in self.players:
            p.drawLetters(self.letters)


    def playGame(self):
        lastTurn = False
        while not lastTurn:
            for player in self.players:
                player.takeTurn()
            if self.letters.getSize == 0:
                lastTurn = True


