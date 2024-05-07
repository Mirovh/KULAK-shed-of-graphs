#!/bin/bash

# Number of batches to split the graphs into
NUM_BATCHES=10

# Directory where the output files will be stored
OUTPUT_DIR="$HOME/filtered-graphs"

# Create the output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Function to run Plantri with the appropriate res/mod and filter
run_plantri() {
    local RES=$1
    local MOD=$2
    local FILTER=$3

    # Run Plantri with the res/mod function and the filter
    plantri -m4 -c1:$RES:$MOD | filter -T -F "$FILTER" > "$OUTPUT_DIR/graphs_$RES.txt"
}

# Export the function so it can be used by parallel
export -f run_plantri

# Run the batches in parallel
seq 0 $((NUM_BATCHES-1)) | parallel run_plantri {} $NUM_BATCHES "your_filter_here"