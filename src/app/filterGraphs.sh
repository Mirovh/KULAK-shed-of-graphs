#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <order> <filter_string/json>"
    exit 1
fi

# Assign arguments to variables
order=$1
filter_string=$2

# Run Plantri with the provided order and flags, and pipe the output to the Python script
plantri -g -p $order | python3 plantriFilter.py "$filter_string"