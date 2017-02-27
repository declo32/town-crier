#!/usr/bin/env bash

cd py

# Order is important
declare -a files=(
    # "Announcement-Scrape.py"
    "Twitter-Scrape.py"
    "Assemble.py"
)

for file in "${files[@]}"
do
    python3 "$file"
done