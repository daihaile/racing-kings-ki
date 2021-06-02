from connection import Bot_interface
import logging
import json
import sys
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_input(argv):
    """
    # Styles of input:
    ## Full input:
    python3 main.py gameurl w||b pl_token

    ## File input (Quickstart, docker-compose)
    python3 main.py w||b
    pl_token is read from json file
    gameurl is guessed from json file (assumes localhost server)
    """
    gameurl, my_color, pl_token = read_input(argv)
    url, game_id = process_gameurl(gameurl)

    if not input_correct(url, game_id,my_color,pl_token):
        logger.critical("input incorrect")
        quit()
    return url, game_id,my_color,pl_token

def read_input(argv):
    if len(argv)==2:
        return read_file_input(pl_color=argv[1])
    elif len(argv)==4:
        return read_param_input(argv)
    else:
        sys.exit("invalid number of parameters")

def read_param_input(argv):
    gameurl = argv[1]
    my_color = argv[2]
    pl_token = argv[3]
    return gameurl, my_color, pl_token

def read_file_input(pl_color):
    with open('game_credentials.json', 'r') as json_file:
        game_cred = json.load(json_file)
        game_id = game_cred["game_id"]
    with open('player_credentials.json', 'r') as json_file:
        player_cred = json.load(json_file)
        pl_token = player_cred[pl_color]["token"]
    gameurl = f'http://localhost:5000/game/{game_id}'

    return gameurl, pl_color, pl_token

def process_gameurl(gameurl):
    #[http://](host[/api])/(game)/(id)
    #baserurl may include the /api subdir if on production server.
    split=gameurl.split('/')
    gameid=split[-1]
    if split[-3]=='api':
        baseurl=split[-4]+'/api'
    else:
        baseurl=split[-3]
    return 'http://'+baseurl, gameid

def input_correct(url, game_id,my_color,pl_token):
    url_correct = Bot_interface.can_connect(url+"/players")
    server=Bot_interface(url)

    game_exists = server.game_exists(game_id)
    if not game_exists: logger.error("Game not recognized by server")

    token_correct = server.token_correct(pl_token)
    if not game_exists: logger.error("Token not recognized by server")

    return url_correct * game_exists * token_correct
