#!/usr/bin/env bash

cd py

# Order is important
declare -a files=(
    "Announcement-Scrape.py"
    "Twitter-Scrape.py"
    "Assemble.py"
)

for file in "${files[@]}"
do
    echo "Running $file"
    sudo python3 "$file"
done