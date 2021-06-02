if [[ "$OSTYPE" == "msys" ]]; then
    echo "build image start"
    echo "=========================================================="
    docker build -t pjki-ki .
    echo "=========================================================="
    echo "build image completed"
    echo "=========================================================="
    echo "run image"
    echo "=========================================================="
    docker run \
    --mount type=bind,source="$(pwd)"/app,target=/usr/app \
    -e GAME_ID=$1 \
    -e PLAYER_COLOR=$2 \
    -e PLAYER_TOKEN=$3 \
    pjki-ki
else
    sudo docker build -t pjki-ki .
    echo "=========================================================="
    echo "build image completed"
    echo "=========================================================="
    echo "run image"
    echo "=========================================================="
    sudo docker run \
    --mount type=bind,source="$(pwd)"/app,target=/usr/app \
    -e GAME_ID=$1 \
    -e PLAYER_COLOR=$2 \
    -e PLAYER_TOKEN=$3 \
    pjki-ki
fi
