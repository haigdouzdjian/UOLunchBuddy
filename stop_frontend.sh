#!/usr/bin/env bash
set -o errexit
set -o errtrace
set -o nounset
set -o pipefail
# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Stop the frontend
echo -e "${YELLOW}Stopping frontend...${NC}"
kill $(ps aux | grep '[i]ndex.js' | awk '{print $2}')
echo -e "${GREEN}Frontend terminated.${NC}"
