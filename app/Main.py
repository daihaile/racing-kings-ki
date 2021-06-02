import json
import logging
import datetime
import time


logging.basicConfig(format = '%(asctime)s - %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p',
                    filemode = 'w',
                    filename = 'example.log',
                    level=logging.DEBUG)

import sys

from connection import Bot_interface
import input_handler
import SSEThread
import timemanager

from ki import KI


logger = logging.getLogger('server_logger')

next_color={
        "w":"b",
        "b":"w"
    }
#The API is inconsistent: w||b, playerA||playerB. We try to stick to w||b
c2p={
        "w":"playerA",
        "b":"playerB"
    }


if __name__ == '__main__':

    print("Bot: Hello!")

    print(sys.argv)
    url, game_id, my_color, pl_token=input_handler.handle_input(sys.argv)


    logger.debug(f'url: {url}')
    logger.debug(f'game_id: {game_id}')
    logger.debug(f'my_color: {my_color}')
    logger.debug(f'pl_token: {pl_token}')


    #inizialize variables
    server = Bot_interface (url)
    currentFEN = server.get_fen(game_id)
    turn=currentFEN.split(' ')[1]
    timeBudget, timeout = server.get_time(game_id, c2p[my_color])
    latest_timestamp = datetime.datetime.min

    ki = KI(currentFEN,timeout)

    logger.debug("Connecting: "+url+'/game/'+game_id+'/events')

    from sseclient import SSEClient
    from threading import Thread
    from queue import Queue

    stream = SSEClient(url+"/game/"+game_id+"/events")
    logger.debug("Connection non-blocking")

    q = Queue(maxsize=0)
    worker = Thread(target=SSEThread.read_server, args=(stream,q))
    worker.setDaemon(True)
    worker.start()

       #Start of main loop
    while(True):
        time.sleep(2) #for debugging
        logger.debug("Entered main loop...")
        msg= SSEThread.find_new_message(q,my_color)
        #msg is a dict from the parsed json server message
        if msg!=None:
            #START MESSAGE HANDLING
            #this part updates: currentFEN, turn, timeout,timeBudget
            #which are needed by the move-generator
            #quit when game is over
            logger.info("msg:\n%s"%msg)
            if msg["type"]=="gameEnd":
                print ("winner: "+msg["details"]["winner"])
                quit()

            if msg["type"]=="timeout":
                #diff can be used for debugging to see if there are considerable
                #differences between the server's time-keeping and the client's
                diff = timeout - msg["details"]["timeout"]
                timeout=msg["details"]["timeout"]

            if msg["type"]=="timeBudget":
                diff = msg["details"]["timeBudget"]
                timeBudget=msg["details"]["timeBudget"]

            if msg["type"]=="serverMessage":
                logger.warning("serverMessage:%s"%msg["details"]["messageText"])

            if msg["type"]=="move":
                timeBudget = server.get_time(game_id,c2p[my_color])
                #print(timeBudget[1])
                currentFEN=msg["details"]["postFEN"]
                turn=currentFEN.split(' ')[1]
                logger.debug(f'turn = {turn}')
            else:
                logger.warning("Unhandled message type: %s"%str(msg))
            #END MESSAGE HANDLING
        if (turn != my_color):
            logger.info("It's not my turn")
            continue
        #if we've come this far this means there are no unhandled messages
        #and it is our turn. Time to think
        logger.info("It's my turn. Thinking...")
        #move, time_hint = ai.best_move(currentFEN)
        if timemanager.havetime(timeout,timeBudget,""):
            print("search for best move with KI")
            #ki.update(currentFEN)
            move_ki = ki.doMove(currentFEN)
            print("found move: ",move_ki )

        #time_hint can be used by the ai to influence the calculations
        #of the timemanager. Maybe you won't need it, it's here as an example
        if timemanager.havetime(timeout,timeBudget,""):
            #commit the move
            #print(move_ki)
            server.send_move(game_id, move_ki, pl_token)
            turn=next_color[turn]
