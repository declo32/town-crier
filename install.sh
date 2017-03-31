#!/usr/bin/env bash

declare -a libs=("beautifulsoup4" "python-twitter" "lxml")

for lib in "${libs[@]}"
do
    sudo pip3 install "$lib"
done