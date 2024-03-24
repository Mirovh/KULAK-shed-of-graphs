#!/bin/bash

# Change to the directory containing the script
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "env-dev" ]; then
    # Create virtual environment if it doesn't exist
    python3 -m venv env-dev
else
    # Remove existing virtual environment
    rm -rf env-dev
    # Create virtual environment
    python3 -m venv env-dev
fi

# Activate virtual environment
source env-dev/bin/activate

# Install requirements
pip install -r requirements-dev.txt

# Deactivate virtual environment
deactivate
