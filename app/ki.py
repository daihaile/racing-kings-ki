import move_calculator
import board
from random import randrange
from datetime import datetime
import threading, time, datetime

class KI:
    def __init__(self, fen=None,timeout=55000):
        self.duration = timeout
        self.initTime = None
        self.currentTime = None
        self.bestMove = {
            "move": "",
            "value": 0
        }
        self.moves = []
        self.boardRep = ""
        self.player = ""
        self.halfmove = ""
        self.fullmove = ""
        self.fen = fen
        self.evaFunction = {
            "q": 1000, # queen
            "k": 1000000000000, # king
            "b": 550, # bishop
            "n": 500, # knight
            "r": 600, # rook
        }
        self.boards = {
            "q": 0, # queen
            "k": 0, # king
            "b": 0, # bishop
            "n": 0, # knight
            "r": 0, # rook
            "wh": 0, # white
            "bl": 0 # black
        }

        if(fen != None):
            self.update(fen)

    def getCurrentBestMove(self):
        if not len(self.moves) == 0:
            move = self.takeBestMove()
        else:
            move = self.doRandomMove()
        print(move)
        return True

    def update(self, fen):
        self.moves = []
        self.initTime = datetime.datetime.now()
        self.boards = board.parse(fen).copy()
        str = fen.split(" ")
        self.boardRep = str[0]
        self.halfmove = str[4]
        self.fullmove = str[5]
        if(str[1] == "w"):
            self.player = "wh"
        elif(str[1] == "b"):
            self.player = "bl"

    def doRandomMove(self):
        res = ""
        while(len(res) < 4):
            res = ""
            firstPos = board.getPositions(self.boards[self.player])
            randomIndex = randrange(len(firstPos))
            res += firstPos[randomIndex]
            moves = board.getMoves(self.boards, res)
            secPos = board.getPositions(moves)
            if(len(secPos) > 0):
                randomIndex = randrange(len(secPos))
                res += secPos[randomIndex]
        return res

    def timeHandle(self):
        start_time = datetime.datetime.now()
        current_time = start_time
        print(start_time)
        while True:
            if (datetime.datetime.now() - current_time).seconds == 1:
                current_time = datetime.datetime.now()
                print(current_time)
                if(current_time - start_time).seconds == 5:
                    print("5 seconds past")
                    raise Exception 



    def doMove(self,fen, depth = 3):
        try:
            self.update(fen)
            winvalue = self.maximiseWithoutCutoff({"boards": self.boards, "path": []}, 1, -100000000000000000000000, 1000000000000000000000, True)
            if(winvalue >= 99999999999999999999999900000):
                print("took winValue", winvalue)
                move = self.takeBestMove(winvalue)
            else:
                self.update(fen)
                value = self.maximise({"boards": self.boards, "path": []}, depth, -100000000000000000000000, 1000000000000000000000, True)
                print("value: ", value)
                move = self.takeBestMove(value)
            if(move == None):
                move = self.doRandomMove()
            print(move)
            return move
        except Exception as e:
            move = self.doRandomMove()
            print(e, "returned random move:" ,move)
            return move
        return self.doRandomMove()


    """
    returns a node with calculated value
    a node has the boards before a move, the move, and a value
    """
    def evaluate(self, node):
        res = 0

        if(node["boards"][self.player] & node["boards"]["k"] & int("0000000000000000000000000000000000000000001111111100000000000000", base = 2)):
            res += 300
        elif(node["boards"][self.player] & node["boards"]["k"] & int("0000000000000000000000000000000011111111000000000000000000000000", base = 2)):
            res += 560
        elif(node["boards"][self.player] & node["boards"]["k"] & int("0000000000000000000000001111111100000000000000000000000000000000", base = 2)):
            res += 660
        elif(node["boards"][self.player] & node["boards"]["k"] & int("0000000000000000111111110000000000000000000000000000000000000000", base = 2)):
            res += 950
        elif(node["boards"][self.player] & node["boards"]["k"] & int("0000000011111111000000000000000000000000000000000000000000000000", base = 2)):
            res += 1100
        elif(node["boards"][self.player] & node["boards"]["k"] & int("1111111100000000000000000000000000000000000000000000000000000000", base = 2)):
            res += 100000000000000000000000000000

        if(node["boards"][board.getOpponent(self.player)] & node["boards"]["k"] & int("0000000000000000000000000000000000000000001111111100000000000000", base = 2)):
            res -= 300
        elif(node["boards"][board.getOpponent(self.player)] & node["boards"]["k"] & int("0000000000000000000000000000000011111111000000000000000000000000", base = 2)):
            res -= 560
        elif(node["boards"][board.getOpponent(self.player)] & node["boards"]["k"] & int("0000000000000000000000001111111100000000000000000000000000000000", base = 2)):
            res -= 660
        elif(node["boards"][board.getOpponent(self.player)] & node["boards"]["k"] & int("0000000000000000111111110000000000000000000000000000000000000000", base = 2)):
            res -= 950
        elif(node["boards"][board.getOpponent(self.player)] & node["boards"]["k"] & int("0000000011111111000000000000000000000000000000000000000000000000", base = 2)):
            res -= 1100
        elif(node["boards"][board.getOpponent(self.player)] & node["boards"]["k"] & int("1111111100000000000000000000000000000000000000000000000000000000", base = 2)):
            res -= 100000000000000000000000000000


        for k in self.boards:
            if(k == "wh" or k == "bl"):
                continue
            else:
                res -= (bin(self.boards[k] & self.boards[self.player]).count("1") - bin(node["boards"][k] & node["boards"][self.player]).count("1")) * self.evaFunction[k]
                res += (bin(self.boards[k] & self.boards[board.getOpponent(self.player)]).count("1") - bin(node["boards"][k] & node["boards"][board.getOpponent(self.player)]).count("1")) * self.evaFunction[k]

        return res

    """
    returns the winner
    if no winner exists it returns an empty string ("")
    """
    def winner(self, boards):
        res = ""
        wincondition = int("1111111100000000000000000000000000000000000000000000000000000000", base = 2)
        if(boards["k"] & boards["wh"] & wincondition >= 1):
            res += "wh"
        elif(boards["k"] & boards["bl"] & wincondition >= 1):
            res += "bl"

        return res

    def takeBestMove(self, value = -99999999999999999999999999999999999999):
        if(value == -99999999999999999999999999999999999999):
            resVal = -1000000000000000000000000000000
            resMov = ""
            for move in self.moves:
                if(move["value"] > resVal):
                    resVal = move["value"]
                    resMov = move["move"]
            return resMov
        else:
            for move in self.moves:
                if(move["value"] == value):
                    return move["move"]



    """
    maximiser function
    """
    def maximise(self, node, depth, alpha, beta, storeMove = False):
        if (datetime.datetime.now() - self.initTime).seconds >= self.duration:
            #print(self.initTime,self.currentTime,(datetime.datetime.now() - self.initTime).seconds)
            raise Exception("Timeout")
        if(depth == 0 or self.winner(node["boards"])):
            return self.evaluate(node)

        positions = []
        positions = board.getPositions(node["boards"][self.player])
        breakout = False
        for pos in positions:
            movePositions = board.getPositions(board.getMoves(node["boards"], pos))
            for movePos in movePositions:
                path = node["path"].copy()
                path.append(pos + movePos)
                value = self.minimise({"boards": board.doMove(self.player, node["boards"], pos + movePos), "path": path}, depth - 1, alpha, beta)
                if(storeMove and value > alpha):
                    self.moves.append({"move": path[0], "value": value})
                alpha = max(alpha, value)


                if(alpha >= beta):
                    breakout = True
                    break
            if(breakout):
                break

        return alpha

    def minimise(self, node, depth, alpha, beta):
        if(depth == 0 or self.winner(node["boards"])):
            return self.evaluate(node)

        positions = board.getPositions(node["boards"][board.getOpponent(self.player)])
        breakout = False
        for pos in positions:
            movePositions = board.getPositions(board.getMoves(node["boards"], pos))
            for movePos in movePositions:
                path = node["path"].copy()
                path.append(pos+movePos)
                beta = min(beta, self.maximise({"boards": board.doMove(board.getOpponent(self.player), node["boards"], pos + movePos), "path": path}, depth - 1, alpha, beta))
                if(beta < alpha):
                    breakout = True
                    break
            if(breakout):
                break

        return beta


    """
     checks the performance for different depths with start Position
     default depth = 5
    """
    def performanceTest(self, depth = 7):
        for i in range(1, depth + 1):
            now = datetime.datetime.now()
            move = self.doMove(i)
            last = datetime.datetime.now()
            print("depth: " + str(i) + ", move: " + move + ", time: " + str(last - now))

    def doMoveWithCutoff(self, depth = 3):
        try:
            value = self.maximiseWithCutoff({"boards": self.boards, "path": []}, depth, -100000000000000000000000, 1000000000000000000000, True)
            #print(value)
            move = self.takeBestMove(value)
            if(move == None):
                move = self.doRandomMove()
            #print(move)
            return move
        except Exception as e:
            print(e)


    def maximiseWithoutCutoff(self, node, depth, alpha, beta, storeMove = False):
        if storeMove:
            self.nodeCount = 1
        else:
            self.nodeCount += 1
        if (datetime.datetime.now() - self.initTime).seconds >= self.duration:
            #print(self.initTime,self.currentTime,(datetime.datetime.now() - self.initTime).seconds)
            raise Exception("Timeout")
        if(depth == 0 or self.winner(node["boards"])):
            return self.evaluate(node)

        positions = []
        positions = board.getPositions(node["boards"][self.player])
        breakout = False
        for pos in positions:
            movePositions = board.getPositions(board.getMoves(node["boards"], pos))
            for movePos in movePositions:
                path = node["path"].copy()
                path.append(pos + movePos)
                value = self.minimiseWithoutCutoff({"boards": board.doMove(self.player, node["boards"], pos + movePos), "path": path}, depth - 1, alpha, beta)
                if(storeMove and value > alpha):
                    self.moves.append({"move": path[0], "value": value})
                alpha = max(alpha, value)

        return alpha

    def minimiseWithoutCutoff(self, node, depth, alpha, beta):
        self.nodeCount += 1
        if(depth == 0 or self.winner(node["boards"])):
            return self.evaluate(node)

        positions = board.getPositions(node["boards"][board.getOpponent(self.player)])
        breakout = False
        for pos in positions:
            movePositions = board.getPositions(board.getMoves(node["boards"], pos))
            for movePos in movePositions:
                path = node["path"].copy()
                path.append(pos+movePos)
                beta = min(beta, self.maximiseWithoutCutoff({"boards": board.doMove(board.getOpponent(self.player), node["boards"], pos + movePos), "path": path}, depth - 1, alpha, beta))

        return beta





"""
main function
"""
if __name__ == "__main__":
    start = "8/8/8/8/8/8/krbnNBRK/qrbnNBRQ w - - 0 1"
    test = "8/5R2/6K1/8/8/2r5/8/8 b - - 0 1"
    testWin = "8/1Q5K/7b/2k5/8/8/6N1/6r1 b - - 0 1"
    ki = KI(start)
    ki.performanceTest()
    #print(ki.evaluate({"boards": board.parse("8/8/8/8/8/8/krbnNBRK/qrbn1BRQ w - - 0 1")}))
    #res = ki.maximise({"boards": ki.boards, "path": []}, 3, -100000000000000000000000, 1000000000000000000000, True)
    #print(ki.doMove(5))

    """
    #tests
    otherKingCheckTest = "8/8/8/4Q3/7R/1k3N2/3K4/5B2 w - - 0 1"
    ownKingCheckTest = "8/5r2/4K3/3BR3/8/1q6/4q3/8 w - - 0 1"
    otherKingTest = "8/4B3/8/2R5/1k2N1R1/8/8/8 w - - 0 1"
    evaCheck = "QRRBB3/qrrbb3/8/8/8/8/8/8 w - - 0 1"
    ki = KI(ownKingCheckTest)
    #print(board.getPositions(ki.boards["wh"]))
    board.printBoard(board.getMoves(ki.boards, "e6"))

python3 Main.py https://pjki.ml/api/game/QVjc4XupKvfOsLEc w 0l45MZT0VWa9Hbc3WwR97AVz4Sj1hVLRa4LTVG1k2n


    """
