#!/bin/bash

# Check if filename is provided
if [ -z "$1" ]; then
  echo "$0 <arquivo> [-min]"
  exit 1
fi

# Set filename as var
FILE=$1

if [ "$2" == "-min" ]; then
    # Sort by fifht field in the line, get first line and print it
    sort -k5 -n $FILE | head -1 | awk "{print $NF}"
else
    sort -k5 -nr $FILE | head -1 | awk "{print $NF}"
fi