#!/usr/bin/env bash
set -o errexit
set -o errtrace
set -o nounset
set -o pipefail
# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color
IMAGE='project2' # Name of docker image
APP='lunchbuddy' # Name of docker container
NOW=$(date +"%d-%m-%Y") # Timestamp
BUILDLOG="BUILD-${NOW}"
RUNLOG="RUN-${NOW}"

echo -e "${YELLOW}Deploying...${NC}"
echo -e "${YELLOW}Building docker image${NC}"
docker build -t ${IMAGE} . 2>&1 | tee ${BUILDLOG}
echo -e "${GREEN}Docker image built successfully.${NC}"
# Check if container isn't running
if [ ! "$(docker ps -q -f name=${APP})" ]; then
    # Check if container is exited
    if [ "$(docker ps -aq -f status=exited -f name=${APP})" ]; then
        # cleanup
        docker rm ${APP}
    fi
    # run container
    echo -e "${YELLOW}Starting docker container${NC}"
    docker run --rm --name ${APP} -d -p 80:3000 -p 8000:2812 ${IMAGE} 2>&1 | tee ${RUNLOG}
    echo -e "${GREEN}Docker container running successfully.${NC}"
else
    # container was already running
    echo -e "${YELLOW}${APP} container is running, restarting...${NC}"
    # cleanup
    docker stop ${APP}
    # run container
    echo -e "${YELLOW}Starting docker container${NC}"
    docker run --rm --name ${APP} -d -p 80:3000 -p 8000:2812 ${IMAGE} 2>&1 | tee ${RUNLOG}
    echo -e "${GREEN}Docker container running successfully.${NC}"
fi
echo -e "${GREEN}Deployment successful. Check status at <host>:8000${NC}"
