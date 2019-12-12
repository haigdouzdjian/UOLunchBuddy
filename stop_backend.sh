#!/usr/bin/env bash
set -o errexit
set -o errtrace
set -o nounset
set -o pipefail
# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Stop the backend
echo -e "${YELLOW}Stopping backend...${NC}"
kill $(ps aux | grep '[b]ackend/api.py' | awk '{print $2}')
echo -e "${GREEN}Backend terminated.${NC}"
