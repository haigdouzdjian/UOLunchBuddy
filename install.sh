#!/usr/bin/env bash
set -o errexit
set -o errtrace
set -o nounset
set -o pipefail
# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Backend install
echo -e "${YELLOW}Installing backend.${NC}"
echo "Creating python environment."
cd ./backend
python3 -m venv env
echo "Activating python environment."
source env/bin/activate
echo "Installing python dependencies."
pip install -r requirements.txt
cd ../
echo -e "${GREEN}Backend installed.${NC}"

# Frontend install
echo -e "${YELLOW}Installing frontend.${NC}"
cd ./frontend
echo "Installing frontend dependencies."
yarn build
cd ../
echo -e "${GREEN}Frontend installed.${NC}"
