#!/bin/bash

#replace localhost with the ip if server is run elsewhere
#HOST=localhost:5000 #local werkzeug
#HOST=localhost:80/api #nginx+uwsgi

HOST=https://pjki.ml/api

if [[ $# -eq 0 ]] ; then
    echo 'Please give rk or js as argument to start the game.'
    exit 0
fi

case "$1" in
    'rk') echo 'Starting Racing Kings!';
          GAME='rk' ;;
    'js') echo 'Starting Jump Sturdy!' ;
          GAME='js';;
    *) echo 'bad argument, please use rk or js.';
        exit 0 ;;
esac


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'READING app/player_credentials.json'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -

PLAYERSINFO=`cat app/player_credentials.json`

PLAYER1ID=`echo ${PLAYERSINFO} | jq -r .w.id`
PLAYER1TOKEN=`echo ${PLAYERSINFO} | jq -r .w.token`

PLAYER2ID=`echo ${PLAYERSINFO} | jq -r .b.id`
PLAYER2TOKEN=`echo ${PLAYERSINFO} | jq -r .b.token`

printf "PLAYER1ID: %s\nPLAYER1TOKEN: %s\n" "$PLAYER1ID" "$PLAYER1TOKEN"
printf "PLAYER2ID: %s\nPLAYER2TOKEN: %s\n" "$PLAYER2ID" "$PLAYER2TOKEN"


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'CREATING GAME'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -

case "$GAME" in
    'rk') TYPE="racingKings";
          INITIALFEN="8/8/8/8/8/8/krbnNBRK/qrbnNBRQ w KQkq - 0 1" ;;
    'js') TYPE="jumpSturdy" ;
          INITIALFEN="1bbbbbb1/1bbbbbb1/8/8/8/8/1BBBBBB1/1BBBBBB1 w KQkq - 0 1";;
esac

#be extra careful, the server expects ints!
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
echo "gameinfo: "$GAMEINFO
GAMEID=`echo ${GAMEINFO} | jq -r .id`

echo ${GAMEID}
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
