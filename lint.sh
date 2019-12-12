#!/usr/bin/env bash
set -o errexit
set -o errtrace
set -o nounset
set -o pipefail
# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Activate python environment
echo -e "${YELLOW}Linting backend.${NC}"
cd ./backend
source env/bin/activate
# Just show the diffs for now
autopep8 -v --diff -a ./*.py
echo -e "${GREEN}Backend linting complete.${NC}"

# Lint frontend
echo -e "${YELLOW}Linting frontend.${NC}"
cd ../frontend
yarn lint
cd ../
echo -e "${GREEN}Frontend linting complete.${NC}"
