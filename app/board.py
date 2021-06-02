import move_calculator
import re



def parse(fen):
    field = fen.split(" ")[0]
    resBoards = {
        "q": 0, # queen
        "k": 0, # king
        "b": 0, # bishop
        "n": 0, # knight
        "r": 0, # rook
        "wh": 0, # white
        "bl": 0 # black
    }

    pos = 0
    for elem in field:
        mask = 9223372036854775808>>pos # 9223372036854775808 == s^63
        if elem == 'K':
            resBoards[elem.lower()] |= mask
            resBoards["wh"] |= mask
            pos += 1
        elif elem == 'B':
            resBoards[elem.lower()] |= mask
            resBoards["wh"] |= mask
            pos += 1
        elif elem == 'N':
            resBoards[elem.lower()] |= mask
            resBoards["wh"] |= mask
            pos += 1
        elif elem == 'R':
            resBoards[elem.lower()] |= mask
            resBoards["wh"] |= mask
            pos += 1
        elif elem == 'Q':
            resBoards[elem.lower()] |= mask
            resBoards["wh"] |= mask
            pos += 1
        elif elem == 'k':
            resBoards[elem.lower()] |= mask
            resBoards["bl"] |= mask
            pos += 1
        elif elem == 'b':
            resBoards[elem.lower()] |= mask
            resBoards["bl"] |= mask
            pos += 1
        elif elem == 'n':
            resBoards[elem.lower()] |= mask
            resBoards["bl"] |= mask
            pos += 1
        elif elem == 'r':
            resBoards[elem.lower()] |= mask
            resBoards["bl"] |= mask
            pos += 1
        elif elem == 'q':
            resBoards[elem.lower()] |= mask
            resBoards["bl"] |= mask
            pos += 1
        elif elem != '/':
            pos += int(elem)
        elif elem == '/' and pos % 8 != 0:
            raise RuntimeError("ParseError: Each line on the board has to contain exactly 8 fields.")

    return resBoards


def doMove(player, boards, move):
    first = move[0] + move[1]
    second = move[2] + move[3]
    figure = getFigure(boards, first).lower()
    b = boards.copy()
    b[figure] = setField(first, 0, boards[figure])
    b[player] = setField(first, 0, boards[player])

    test = setField(second, 1, 0)
    if(test & b[getOpponent(player)] >= 1):
        oppFigure = getFigure(b, second)
        b[getOpponent(player)] = setField(second, 0, b[getOpponent(player)])
        b[oppFigure.lower()] = setField(second, 0, b[oppFigure.lower()])

    b[figure] = setField(second, 1, b[figure])
    b[player] = setField(second, 1, b[player])

    return b


"""
returns all valid moves as a bitboard for a given figure
field = a3, b4, e7, ...
"""

def getMoves(boards, field):
    fig = getFigure(boards, field)
    if(fig == None):
        print("no figure on field")
        return None;

    player = getPlayer(fig)
    b = boards.copy();

    kritFig = [] #every opponent figure, that sets the players king in check, if fig is not on his field
    kritFigOwn = [] #every own figure, that sets the opponent king in check, if fig is not on his field
    isCheck = False
    if(fig.lower() == "k"):
        #goto moves
        pass

    #checks if the own king is in check, when move the figure (players figure is not on the field)
    #checks if the opponent king is in check, "---"
    b[fig.lower()] = setField(field, 0, b[fig.lower()])
    b[player] = setField(field, 0, b[player])
    #get all positions of the opponent figures
    positions = getPositions(b[getOpponent(player)])
    positionsOwn = getPositions(b[player])

    #get all own figures with index (x,y), that sets the opponent king in check
    #if one figure is able to set the opponent king in check return 0
    for pos in positionsOwn:
        x = 7-int(ord(pos[0].lower())-ord("a"));
        y = int(pos[1])-1;
        figure = getFigure(boards, pos);
        if((b["k"] & b[getOpponent(player)]) & move_calculator.getMoves(figure.lower(), b, player, x, y, False) >= 1):
            kritFigOwn.append([figure, x, y])
            return 0

    #get all opponent figures with index (x,y), that sets the players king in check
    for pos in positions:
        x = 7-int(ord(pos[0].lower())-ord("a"));
        y = int(pos[1])-1;
        opponentFigure = getFigure(boards, pos);
        if((b["k"] & b[player]) & move_calculator.getMoves(opponentFigure.lower(), b, getOpponent(player), x, y, False) >= 1):
            kritFig.append([opponentFigure, x, y])

    #checks if the opponent king is in check, when move the figure
    if(len(kritFig) > 0):
        #gets all moves of the current figure of the player without an opposing figure being able to set the player king in check
        x = 7-int(ord(field[0].lower())-ord("a"));
        y = int(field[1])-1;
        #gets all moves of the current figure
        allMoves = getPositions(move_calculator.getMoves(fig, boards, player, x, y, True))
        bMove = b.copy();
        res1 = 0
        #goes through all position and check
        for pos in allMoves:
            bMove[fig.lower()] = setField(pos, 1, b[fig.lower()])
            bMove[player] = setField(pos, 1, b[player])
            x = 7-int(ord(pos[0].lower())-ord("a"));
            y = int(pos[1])-1;
            for figure in kritFig:
                isCheck = False
                mov = move_calculator.getMoves(figure[0].lower(), bMove, getOpponent(player), figure[1], figure[2], False)
                #check if the current figure can beat the opponent
                if((bMove[player] & bMove[fig.lower()]) & (1 << (figure[1] + 8*figure[2])) > 0):
                    continue
                #check if the opponent figure can reach the players king
                elif((b[player] & b["k"]) & mov > 0):
                    isCheck = True
            if(not isCheck):
                res1 = res1 | 1 << (x + 8*y)

        """
        #gets all moves of the current figure of the player without an own figure being able to set the opponent king in check
        x = 7-int(ord(field[0].lower())-ord("a"));
        y = int(field[1])-1;
        #gets all moves of the current figure
        allMoves = getPositions(move_calculator.getMoves(fig, boards, player, x, y, True))
        bMove = b.copy();
        res2 = 0
        #goes through all position and check
        for pos in allMoves:
            bMove[fig.lower()] = setField(pos, 1, b[fig.lower()])
            bMove[player] = setField(pos, 1, b[player])
            x = 7-int(ord(pos[0].lower())-ord("a"));
            y = int(pos[1])-1;
            for figure in kritFigOwn:
                isCheck = False
                mov = move_calculator.getMoves(figure[0].lower(), bMove, player, figure[1], figure[2], False)
                #check if the own figure can reach the opponent king
                if((b[getOpponent(player)] & b["k"]) & mov > 0):
                    isCheck = True
            if(not isCheck):
                res2 = res2 | 1 << (x + 8*y)
        """



    #label .moves
    if(len(kritFig) > 0):
        return res1
    else:
        x = 7-int(ord(field[0].lower())-ord("a"));
        y = int(field[1])-1;
        return move_calculator.getMoves(fig, boards, player, x, y, True)


"""
returns the opponent
"""
def getOpponent(player):
    if(player == "wh"):
        return "bl"
    else:
        return "wh"

"""
returns black or white player for a given figure (r, B, ...)
"""
def getPlayer(figure):
    if(figure.lower() == figure):
        return "bl"
    else:
        return "wh"

"""
returns a figure (k, q, K, B, ...) for a given field (a3, b4, e7, ...)
"""
def getFigure(boards, field):
    position = field[0].lower() + field[1]
    m = re.compile("[a-h][1-8]").match(position)

    if m is None:
        raise SyntaxError("The Syntax of the position is wrong! string:" + start)

    x = 7-int(ord(field[0].lower())-ord("a"))
    y = int(field[1])-1
    pos = y*8+x
    mask = 1 << pos
    for b in boards:
        if b in ["wh", "bl"]:
            continue

        if bool(boards[b] & mask):
            if bool(boards["wh"] & mask):
                return b.upper()
            elif bool(boards["bl"] & mask):
                return b.lower()
            break

    return None


"""
return all positions ([e2, f4, a3, ...]) of figures for a bitboard
"""
def getPositions(board):
    res = []
    b = int(board)
    for i in range(64):
        if(b == 0):
            break
        #shift board right and get carry bit
        b, carry = b>>1, b&1
        if(carry == 1):
            #get x and y
            y = int(i / 8)
            x = chr(ord("h") - (i - (y * 8)))
            res.append(str(x) + str(y + 1))

    return res

"""
sets a field(e2, a4, f6, ...) on a bitboard to value 1 or 0
returns the bitboard
"""
def setField(field, value, board):
    if(value != 0 and value != 1):
        print("setField: value has to be an int '1' or '0'")
        return None

    #get x and y of the field
    x = 7-int(ord(field[0].lower())-ord("a"));
    y = int(field[1])-1;
    res = 0
    for i in range(64):
        if(i == x + (y * 8)):
            res = res | value<<i
        elif(board & (1 << i)):
            res = res | 1 << i

    return res


def printBoard(board):
    str = '{0:b}'.format(board).zfill(64)
    res = "";
    i = 1;
    for elem in str:
        res += elem;
        if(i % 8 == 0):
            res += "\n"
        i += 1

    print(res)



    #move_calculator.test()
