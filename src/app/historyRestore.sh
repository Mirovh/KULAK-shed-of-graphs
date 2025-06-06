#!/bin/bash

# Directory where the history file is located
DIR="∼/.filtered-graphs"

# List all backup files
BACKUPS=($(ls $DIR/backup_*))

# Print all available backups
echo "Available backups:"
for i in "${!BACKUPS[@]}"; do
    echo "$i: ${BACKUPS[$i]}"
done

# Ask the user to choose a backup
read -p "Enter the number of the backup you want to restore: " CHOICE

# Restore the chosen backup
cp "${BACKUPS[$CHOICE]}" "$DIR/history.pkl"
