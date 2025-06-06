#!/bin/bash

# Directory where the history file is located
DIR="∼/.filtered-graphs"

# While loop to continuously create backups
while true; do
    # Create a unique filename based on the current date and time
    FILENAME="backup_$(date +'%Y%m%d_%H%M%S').pkl"
    
    # Copy the history file to a new backup file
    cp "$DIR/history.pkl" "$DIR/$FILENAME"
    
    # Wait for one hour (3600 seconds)
    sleep 3600
done
