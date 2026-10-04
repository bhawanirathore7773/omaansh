#!/bin/bash

# HOOVALE Startup Script
# This script helps setup and run the Django application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     HOOVALE - Django Startup Script     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}\n"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}\n"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}\n"
fi

# Activate virtual environment
source venv/bin/activate || . venv/Scripts/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}\n"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please update .env file with your configuration${NC}\n"
fi

# Create logs directory
mkdir -p logs
echo -e "${GREEN}✓ Logs directory ready${NC}\n"

# Create media directory
mkdir -p media/products
mkdir -p media/categories
mkdir -p media/og_images
echo -e "${GREEN}✓ Media directories created${NC}\n"

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py migrate --noinput
echo -e "${GREEN}✓ Migrations completed${NC}\n"

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput -q
echo -e "${GREEN}✓ Static files collected${NC}\n"

# Display menu
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Select an option:${NC}"
echo "1) Run development server"
echo "2) Create superuser"
echo "3) Run tests"
echo "4) Shell"
echo "5) Exit"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo -e "\n${GREEN}Starting development server...${NC}"
        echo -e "${YELLOW}Access at: http://localhost:8000${NC}"
        echo -e "${YELLOW}Admin at: http://localhost:8000/admin${NC}\n"
        python manage.py runserver
        ;;
    2)
        echo -e "\n${YELLOW}Create superuser account${NC}"
        python manage.py createsuperuser
        ;;
    3)
        echo -e "\n${YELLOW}Running tests...${NC}"
        python manage.py test
        ;;
    4)
        echo -e "\n${YELLOW}Starting Django shell...${NC}"
        python manage.py shell
        ;;
    5)
        echo -e "\n${GREEN}Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "\n${RED}Invalid choice${NC}"
        exit 1
        ;;
esac
