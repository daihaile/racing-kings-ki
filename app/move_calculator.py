import board

"""
call the function for the given figure
control is used to enable the isCheck function (there are cases where you not want to check for chess)
"""
def getMoves(fig, boards, player, x, y, control):

    if(fig.lower() == "r"):
        return movesRook(boards, player, x, y, control)
    elif(fig.lower() == "b"):
        return movesBishop(boards, player, x, y, control)
    elif(fig.lower() == "q"):
        return movesQueen(boards, player, x, y, control)
    elif(fig.lower() == "k"):
        return movesKing(boards, player, x, y, control)
    elif(fig.lower() == "n"):
        return movesKnight(boards, player, x, y, control)

def movesQueen(boards, player, x, y, control):
    res = 0

    res = res | movesRook(boards, player, x, y, control, "q")
    res = res | movesBishop(boards, player, x, y, control, "q")

    return res


def movesRook(boards, player, x, y, control, fig = "r"):
    res = 0
    xWalk = x
    yWalk = y
    yWalk += 1
    while(yWalk >= 0 and yWalk < 8 and xWalk >= 0 and xWalk < 8):
        #checks if the field is blocked by an figure of the player
        if((player == "wh" and (int(boards["wh"]) & (1 << (xWalk + 8*yWalk))) > 0) or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl")):
            break;
        #checks if a opponent figure is on this field
        elif((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh")):
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                break
            #beats the opponent figure and dont goes ahead
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                break
        #goes ahead
        else:
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                yWalk += 1
                continue
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                yWalk += 1

    xWalk = x
    yWalk = y
    yWalk -= 1
    while(yWalk >= 0 and yWalk < 8 and xWalk >= 0 and xWalk < 8):
        if((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl")):
            break;
        elif((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh")):
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                break
            #beats the opponent figure and dont goes ahead
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                break
        #goes ahead
        else:
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                yWalk -= 1
                continue
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                yWalk -= 1

    xWalk = x
    yWalk = y
    xWalk += 1
    while(yWalk >= 0 and yWalk < 8 and xWalk >= 0 and xWalk < 8):
        if((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl")):
            break;
        elif((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh")):
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                break
            #beats the opponent figure and dont goes ahead
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                break
        #goes ahead
        else:
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                xWalk += 1
                continue
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                xWalk += 1

    xWalk = x
    yWalk = y
    xWalk -= 1
    while(yWalk >= 0 and yWalk < 8 and xWalk >= 0 and xWalk < 8):
        if((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl")):
            break;
        elif((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh")):
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                break
            #beats the opponent figure and dont goes ahead
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                break
        #goes ahead
        else:
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                xWalk -= 1
                continue
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                xWalk -= 1

    return res

"""
returns a bitboard of all valid moves of Bishop
checks every line (top right, top left, down rigth, down left)
"""
def movesBishop(boards, player, x, y, control, fig = "b"):
    res = 0

    #walks up to the right
    xWalk = x
    yWalk = y
    yWalk += 1
    xWalk += 1
    while(yWalk >= 0 and yWalk < 8 and xWalk >= 0 and xWalk < 8):
        #checks if the field is blocked by a figure of the player
        if((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl")):
            break;
        #checks if a opponent figure is on this field
        elif((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh")):
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                break
            #beats the opponent figure and dont goes ahead
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                break
        #goes ahead
        else:
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                xWalk += 1
                yWalk += 1
                continue
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                xWalk += 1
                yWalk += 1



    #walks down to the left
    xWalk = x
    yWalk = y
    yWalk -= 1
    xWalk -= 1
    while(yWalk >= 0 and yWalk < 8 and xWalk >= 0 and xWalk < 8):
        if((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl")):
            break;
        elif((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh")):
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                break
            #beats the opponent figure and dont goes ahead
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                break
        #goes ahead
        else:
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                xWalk -= 1
                yWalk -= 1
                continue
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                xWalk -= 1
                yWalk -= 1

    #walks down to the right
    xWalk = x
    yWalk = y
    xWalk += 1
    yWalk -= 1
    while(yWalk >= 0 and yWalk < 8 and xWalk >= 0 and xWalk < 8):
        if((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl")):
            break;
        elif((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh")):
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                break
            #beats the opponent figure and dont goes ahead
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                break
        #goes ahead
        else:
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                xWalk += 1
                yWalk -= 1
                continue
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                xWalk += 1
                yWalk -= 1

    #walks up to the left
    xWalk = x
    yWalk = y
    xWalk -= 1
    yWalk += 1
    while(yWalk >= 0 and yWalk < 8 and xWalk >= 0 and xWalk < 8):
        if((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl")):
            break;
        elif((int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh")):
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                break
            #beats the opponent figure and dont goes ahead
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                break
        #goes ahead
        else:
            #checks if the opponent king is in check for this field
            if(control and isCheck(boards, fig, player, xWalk, yWalk)):
                xWalk -= 1
                yWalk += 1
                continue
            else:
                res = res | (1 << (xWalk + 8*yWalk));
                xWalk -= 1
                yWalk += 1

    return res

def movesKing(boards, player, x, y, control):
    res = 0;
    xWalk = x
    yWalk = y

    for i in range(8):
        xWalk = x
        yWalk = y
        if(i == 0):
            yWalk += 1
        elif(i == 1):
            xWalk += 1
            yWalk += 1
        elif(i == 2):
            xWalk += 1
        elif(i == 3):
            xWalk += 1
            yWalk -= 1
        elif(i == 4):
            yWalk -= 1
        elif(i == 5):
            xWalk -= 1
            yWalk -= 1
        elif(i == 6):
            xWalk -= 1
        elif(i == 7):
            xWalk -= 1
            yWalk += 1

        if(yWalk < 0 or yWalk >= 8 or xWalk < 0 or xWalk >= 8 or (int(boards[player]) & (1 << (xWalk + 8*yWalk)) > 0)):
            pass
        elif(control and isOwnKingCheck(boards, player, xWalk, yWalk)):
            pass
        elif(control):
            if(isCheck(boards, "k", player, xWalk, yWalk)):
                pass
            else:
                res = res | (1 << (xWalk + 8*yWalk));
        else:
            res = res | (1 << (xWalk + 8*yWalk));

    return res

def movesKnight(boards, player, x, y, control):
    res = 0
    xWalk = x
    yWalk = y

    for i in range(8):
        xWalk = x
        yWalk = y
        if(i == 0):
            xWalk += 1
            yWalk += 2
        elif(i == 1):
            xWalk += 2
            yWalk += 1
        elif(i == 2):
            xWalk += 2
            yWalk -= 1
        elif(i == 3):
            xWalk += 1
            yWalk -= 2
        elif(i == 4):
            xWalk -= 1
            yWalk -= 2
        elif(i == 5):
            xWalk -= 2
            yWalk -= 1
        elif(i == 6):
            xWalk -= 2
            yWalk += 1
        elif(i == 7):
            xWalk -= 1
            yWalk += 2

        if(yWalk < 0 or yWalk >= 8 or xWalk < 0 or xWalk >= 8 or (int(boards["wh"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "wh") or (int(boards["bl"]) & (1 << (xWalk + 8*yWalk)) > 0 and player == "bl")):
            pass
        elif(control):
            if(isCheck(boards, "n", player, xWalk, yWalk)):
                pass
            else:
                res = res | (1 << (xWalk + 8*yWalk));
        else:
            res = res | (1 << (xWalk + 8*yWalk));

    return res

"""
returns true if opponent king is in check
returns false if opponent king is not in check
do a move and check if the figure can reach the field of the opponent king
"""
def isCheck(boards, fig, player, x, y):
    check = 0;
    if(player == "wh"):
        if(fig == "k"):
            check = (int(boards["k"]) & int(boards["bl"])) & movesKing(boards, player, x, y, False)
        elif(fig == "n"):
            check = (int(boards["k"]) & int(boards["bl"])) & movesKnight(boards, player, x, y, False)
        elif(fig == "q"):
            check = (int(boards["k"]) & int(boards["bl"])) & movesQueen(boards, player, x, y, False)
        elif(fig == "b"):
            check = (int(boards["k"]) & int(boards["bl"])) & movesBishop(boards, player, x, y, False)
        elif(fig == "r"):
            check = (int(boards["k"]) & int(boards["bl"])) & movesRook(boards, player, x, y, False)
    elif(player == "bl"):
        if(fig == "k"):
            check = (int(boards["k"]) & int(boards["wh"])) & movesKing(boards, player, x, y, False)
        elif(fig == "n"):
            check = (int(boards["k"]) & int(boards["wh"])) & movesKnight(boards, player, x, y, False)
        elif(fig == "q"):
            check = (int(boards["k"]) & int(boards["wh"])) & movesQueen(boards, player, x, y, False)
        elif(fig == "b"):
            check = (int(boards["k"]) & int(boards["wh"])) & movesBishop(boards, player, x, y, False)
        elif(fig == "r"):
            check = (int(boards["k"]) & int(boards["wh"])) & movesRook(boards, player, x, y, False)

    if(check >= 1):
        return True
    else:
        return False

"""
checks if the players king is in check if he would do this move
"""
def isOwnKingCheck(boards, player, x, y):
    b = boards.copy()
    positions = board.getPositions(b[board.getOpponent(player)])
    posKing = board.getPositions(1 << (x + 8*y))[0]
    #if the king is on a field with a opponent figure then delete figure and check if king is reachable
    if(posKing in positions):
        fig = board.getFigure(b, posKing)
        b[board.getOpponent(player)] = board.setField(posKing, 0, b[board.getOpponent(player)])
        b[fig] = board.setField(posKing, 0, b[fig.lower()])
        positions = board.getPositions(b[board.getOpponent(player)])

    #for all opponents positions of figures check if the king is reachable
    for pos in positions:
        xO = 7-int(ord(pos[0].lower())-ord("a"));
        yO = int(pos[1])-1;
        moves = getMoves(board.getFigure(b, pos), b, board.getOpponent(player), xO, yO, False)
        if(moves & 1 << (x + 8*y)):
            return True

    return False
