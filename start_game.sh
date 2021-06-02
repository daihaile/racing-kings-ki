#!/bin/bash
SCRIPT_PATH="./new_game.sh"
HOST=https://pjki.ml/api #local werkzeug

echo $SCRIPT_PATH
(exec "$SCRIPT_PATH" "rk")

COLOR='b'

PLAYERSINFO=`cat app/player_credentials.json`

PLAYER1ID=`echo ${PLAYERSINFO} | jq -r .w.id`
PLAYER1TOKEN=`echo ${PLAYERSINFO} | jq -r .w.token`

PLAYER2ID=`echo ${PLAYERSINFO} | jq -r .b.id`
PLAYER2TOKEN=`echo ${PLAYERSINFO} | jq -r .b.token`


TYPE="racingKings"
INITIALFEN="8/8/8/8/8/8/krbnNBRK/qrbnNBRQ w KQkq - 0 1"

TIMEBUDGET="120000"
TIMEOUT="60000"

GAMEINFO=`echo '
{
  "name": "Finale",
  "type":'\"${TYPE}\"',
  "players": {
    "playerA": {
      "id":'\"${PLAYER1ID}\"',
      "timeout":'${TIMEOUT}',
      "initialTimeBudget":'${TIMEBUDGET}'
    },
    "playerB": {
      "id": '\"${PLAYER2ID}\"',
      "timeout":'${TIMEOUT}',
      "initialTimeBudget":'${TIMEBUDGET}'
    }
  },
  "settings": {
    "initialFEN": '\"${INITIALFEN}\"'
  }
}
' | http POST ${HOST}/games`
#echo "gameinfo: "$GAMEINFO
GAMEID=`echo ${GAMEINFO} | jq -r .id`

#echo ${GAMEID}
GAMEIDJSON='{
    "game_id":"'$GAMEID'",
    "type":"'$TYPE'",
    "initial_FEN":"'$INITIALFEN'",
    "playerA_id":"'$PLAYER1ID'",
    "playerB_id":"'$PLAYER2ID'"
}'
echo "writing to game_credentials.json"
echo ${GAMEIDJSON} | jq '.' > app/game_credentials.json

http -v ${HOST}/games
http -v ${HOST}/game/${GAMEID}


#printf "PLAYER: %s\PLAYERTOKEN: %s\n" "$PLAYER1ID" "$PLAYER1TOKEN"
#printf "BOT: %s\BOTTOKEN: %s\n" "$PLAYER2ID" "$PLAYER2TOKEN"
printf "PLAYERTOKEN: %s\n" "$PLAYER1TOKEN"

printf "$HOST/games/${GAMEID}"
python3 app/Main.py "${HOST}/api/game/${GAMEID}" "$COLOR" "$PLAYER2TOKEN" 
