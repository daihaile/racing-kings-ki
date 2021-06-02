#!/bin/bash

#replace localhost with the ip if server is run elsewhere
HOST=localhost:5000 #local werkzeug
#HOST=localhost:80/api #nginx+uwsgi
TEAMNAME="Team B"
ISISNAME="Gruppe 7"
TYPE="racingKings"
PLAYER1NAME="A"
PLAYER2NAME="B"

if [[ $# -eq 0 ]] ; then
    echo 'Please give rk or js as argument to create a team with players.'
    exit 0
fi

if [[ $# -eq 1 ]] || [[$# -eq 5]]; then
    case "$1" in
        'rk') echo 'Created a Racing Kings team';
            TYPE="racingKings" ;;
        'js') echo 'Created a Jump Sturdy team' ;
            TYPE='jumpSturdy';;
        *) echo 'You gave wrong argument for game type, please use rk or js.';
            exit 0 ;;
    esac;
    if [[ $# -eq 5 ]]; then
        TEAMNAME="$2";
        ISISNAME="$3";
        PLAYER1NAME="$4";
        PLAYER2NAME="$5";
    fi
else
    echo "Illegal number of parameters, please the give following arguments:
     game_type(rk||js) team_name isis_name player1_name player2_name"
    exit 0
fi


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'CREATING GROUP'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -

TEAMINFO=`echo '
{
	"name":'\"${TEAMNAME}\"',
	"isisName":'\"${ISISNAME}\"',
	"type":'\"${TYPE}\"'
}
' | http POST ${HOST}/teams`

TEAMID=`echo ${TEAMINFO} | jq -r .id`
TEAMTOKEN=`echo ${TEAMINFO} | jq -r .token`

echo TEAMID: ${TEAMID}
echo TEAMTOKEN${TEAMTOKEN}

http -v ${HOST}/teams
http -v ${HOST}/team/${TEAMID}


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'CREATING PLAYER 1'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


PLAYER1INFO=`echo '
{
        "name":'\"${PLAYER1NAME}\"'
}
' | http POST ${HOST}/players "Authorization: Basic ${TEAMTOKEN}"`

PLAYER1ID=`echo ${PLAYER1INFO} | jq -r .id`
PLAYER1TOKEN=`echo ${PLAYER1INFO} | jq -r .token`

echo PLAYER1ID: ${PLAYER1ID}
echo PLAYER1TOKEN: ${PLAYER1TOKEN}

http -v ${HOST}/players
http -v ${HOST}/player/${PLAYER1ID}


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'CREATING PLAYER 2'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


PLAYER2INFO=`echo '
{
        "name":'\"${PLAYER2NAME}\"'
}
' | http POST ${HOST}/players "Authorization: Basic ${TEAMTOKEN}"`


PLAYER2ID=`echo ${PLAYER2INFO} | jq -r .id`
PLAYER2TOKEN=`echo ${PLAYER2INFO} | jq -r .token`

echo ${PLAYER2ID}
echo ${PLAYER2TOKEN}

http -v ${HOST}/players
http -v ${HOST}/player/${PLAYER2ID}

PLAYER_CREDENTIALS='{"w":'$PLAYER1INFO',"b":'$PLAYER2INFO'}'
echo "writing to player_credentials.json"
echo $PLAYER_CREDENTIALS | jq '.' > app/player_credentials.json
