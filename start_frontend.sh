#!/usr/bin/env bash
set -o errexit
set -o errtrace
set -o nounset
set -o pipefail
# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Start the frontend
echo -e "${YELLOW}Starting frontend...${NC}"
cd ./frontend
yarn start &
sleep 3
CLIENT_PID=$(ps aux | grep '[i]ndex.js' | awk '{print $2}')
cd ../
echo -e "${GREEN}Frontend started. PID=${CLIENT_PID}${NC}"
