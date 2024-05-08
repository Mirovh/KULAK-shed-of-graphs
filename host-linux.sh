#!/bin/bash

# Change to the directory containing the script
cd "$(dirname "$0")"

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
