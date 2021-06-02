import json
import logging
import requests
import sys
logger = logging.getLogger('server_logger')
class Bot_interface:
    url=None
    def __init__(self, url):
        self.url=url
    # Post requests
    def post(self, subdir, data, token=None):
        if token:
            resp= requests.post(self.url+subdir, data,
            headers={'Authorization': f'Basic {token}'})
        else:
            resp= requests.post(self.url+subdir, data)

        try:
            return resp.json()
        except (ValueError):#json error
            logger.warning(f'Got invalid JSON at POST {self.url+subdir}\
            response: {resp} {resp.content}')
            return {}

    def send_move(self,game_id, move, pl_token):
        json_move=self.move_to_json(move)
        print(json_move)
        move_r=self.post('/game/'+game_id+'/events', json_move, pl_token)
        logger.info(json_move)
        if move_r['valid']==False:
            print(move_r)
            sys.exit(f'Server did not approve move {move}')
            logger.warning("MOVE_R",move_r)

    # GET requests
    def get(self, subdir, token=None):
        if token:
            resp= requests.get(self.url+subdir,headers={'Authorization': f'Basic {token}'})
        else:
            resp= requests.get(self.url+subdir)
        try:
            dict=resp.json()
        except (ValueError):#json error
            logger.warning(f'Got invalid JSON at GET {self.url+subdir}')
        return dict

    def get_fen(self, game_id):
        return self.get('/game/'+game_id)['state']['fen']

    def get_time(self, game_id,player):
        gameinfo_r=self.get('/game/'+game_id)
        timeBudget = gameinfo_r['players'][player]['timeBudget']
        timeout = gameinfo_r['players'][player]['timeout']
        return timeBudget, timeout
    def token_correct(self, pl_token):
        return self.get('/playerlogin', pl_token)['valid']

    def game_exists(self, game_id):
        return requests.get(self.url+'/game/'+game_id).ok

    @staticmethod
    def can_connect(test_url):
        """A function to test if connection can be made without crashing"""
        try:
            requests.get(test_url)
        except (OSError):#connection error
            logger.warning('couldn\'t reach server on: {test_url}')
            return False
        return True
    @staticmethod
    def move_to_json(move):
        jsonmove={
            	'type': 'move',
            	'details': {
            		'move': move
            	 }
            }
        return json.dumps(jsonmove)
