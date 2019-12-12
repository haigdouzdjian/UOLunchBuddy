#!/usr/bin/env bash
set -o errexit
set -o errtrace
set -o nounset
set -o pipefail
# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Start the backend
echo -e "${YELLOW}Starting backend...${NC}"
cd ./backend
source env/bin/activate
python api.py &
sleep 5
API_PID=$(ps aux | grep '[b]ackend/api.py' | awk '{print $2}')
cd ../
echo -e "${GREEN}Backend started. PID=${API_PID}${NC}"
