import dateutil.parser
import queue
import json
import logging
logger = logging.getLogger(__name__)

def dict2pretty(dict):
    return json.dumps(dict, sort_keys=True, indent=4)

def read_server(stream, q):
    """This function is to be run as a separate thread, because waiting for
    the server to send messages blocks the process. This function enters a
    cycle that is not supposed to end
    #
    #     arguments:
    #     stream -- an sseclient object. See https://pypi.org/project/sseclient/
    #     q -- queue for message passing between this and the main thread
    #
    #     returns None as first param if no new message is found
    #     """
    for msg in stream:
        msg=str(msg)
        msg_dict={}
        try:
            msg_dict = json.loads(msg)
        except ValueError as e:
            logger.error("read_server: caught invalid json:\n%s"%msg)
            logger.error(e)
            continue
        logger.info("read_server: new message arrived!")

        q.put(msg_dict)
        q.join()
    logger.error("read_server: Error, why did the stream stop?")

def find_new_message(q,my_color):
    """Polls the Queue q for new messages. Works in tandem with read_server
    #     arguments:
    #     q -- queue for message passing between this and the main thread
    #     returns None if no new message is found
    #     """
    msg=None
    logger.debug("find_new_message: waiting for access to queue")
    try:
      msg=q.get(block=False)
      q.task_done()
      logger.debug("find_new_message: got a new message:\n%s"%dict2pretty(msg))
      myPlayer = "playerA"
      if(my_color == "b"):
          myPlayer = "playerB"

      if(msg["player"] != myPlayer):
          print("opponent move: ", msg["details"]["move"])

    except queue.Empty:
      logger.debug("find_new_message: no new messages")

    return msg
