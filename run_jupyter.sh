#!/bin/bash

source .env

if [ -z "$1" ]; then
	MODE=-it
	RUN_ARGS=/startup.sh
	NEW_PORTS="-p 8888:8888 -p 8787:8787 -p 8686:8686 -p 8585:8585"
else
	MODE=-it
	RUN_ARGS=$@
fi

docker container run ${RUN_OPTS} ${CONTAINER_NAME} ${MODE} ${NETWORK} ${PORT_MAP} ${NEW_PORTS} ${VOL_MAP} ${REGISTRY}${IMAGE}${TAG} ${RUN_ARGS}
