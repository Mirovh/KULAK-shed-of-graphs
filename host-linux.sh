#!/bin/bash

# Change to the directory containing the script
cd "$(dirname "$0")"

# Create the history folder if it doesn't exist
mkdir -p src/app/history
mkdir -p src/app/history/images
# Create an empty history file if it doesn't exist
touch src/app/history/history.pkl

# Check if virtual environment exists
if [ ! -d "env" ]; then
    # Create virtual environment if it doesn't exist
    python3 -m venv env
else
    # Remove existing virtual environment
    rm -rf env
    # Create virtual environment
    python3 -m venv env
fi

# Activate virtual environment
source env/bin/activate

# Install requirements
pip install -r requirements.txt

# Run Python script
python3 src/app/hostServer.py

# Deactivate virtual environment
deactivate
