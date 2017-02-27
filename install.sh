#!/usr/bin/env bash

declare -a libs=("beautifulsoup4" "python-twitter")

for lib in "${libs[@]}"
do
    pip install "$lib"
done