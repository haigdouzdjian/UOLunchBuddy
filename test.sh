#!/usr/bin/env bash
set -o errexit
set -o errtrace
set -o nounset
set -o pipefail
# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Static tests
echo -e "${YELLOW}Running lint.sh${NC}"
./lint.sh
echo -e "${GREEN}lint.sh ran successfully.${NC}"
# Backend tests
echo -e "${YELLOW}Testing backend.${NC}"
cd ./backend
source env/bin/activate
# Start API service
python api.py &
sleep 5
# Run backend test
python testing_backend.py
echo -e "${YELLOW}Backend test complete.${NC}"
# Test API service
python test_api.py
echo -e "${YELLOW}API test complete.${NC}"
# Kill API service
kill $(ps aux | grep '[b]ackend/api.py' | awk '{print $2}')
echo -e "${YELLOW}API service terminated.${NC}"
cd ../
echo -e "${GREEN}Testing complete.${NC}"
