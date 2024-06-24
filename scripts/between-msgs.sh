#!/bin/bash

FILE=$1 # Filename
MIN_MSGS=$2 # Min msg quantity
MAX_MSGS=$3 # Max msg quantity

# Print the lines that are between the range
awk -v min="$MIN_MSGS" -v max="$MAX_MSGS" '{
    size=$5
    if (size >= min && size <= max) {
        print $0
    }
}' $FILE