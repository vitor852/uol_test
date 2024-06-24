#!/bin/bash

# Check if filename is provided
if [ -z "$1" ]; then
  echo "$0 <arquivo>"
  exit 1
fi

# Set filename as var
FILE=$1

if [ "$2" == "-desc" ]; then
    # Sort by the first field (reverse)
    sort -k1,1r $FILE
else
    # Sort by the first field
    sort -k1,1 $FILE
fi