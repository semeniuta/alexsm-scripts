#!/bin/sh

# Remove auxillary LaTeX-produced files from the current directory

masks=("*.aux" "*.log" "*.synctex.gz" "*.bbl" "*.blg")

for mask in "${masks[@]}"
do

    if ls $mask 1> /dev/null 2>&1; then
        echo "Removing $mask"
        rm $mask
    fi

done