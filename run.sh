#!/usr/bin/env bash

# Parse arguments

DISPLAYTIME=28800
for i in "$@"; do
	case $i in
		--display-time=*)
		DISPLAYTIME="${i#*=}"
		shift
		;;
		
		*)
		echo "$i isn't a thing"
	esac
done

echo "DISPLAYTIME = ${DISPLAYTIME}"

# Get info

cd py

# Order is important
declare -a files=(
    "Announcement-Scrape.py"
    "Twitter-Scrape.py"
    "Assemble.py"
)

for file in "${files[@]}"; do
    echo "Running ${file}"
    sudo python3 "${file}"
done

# Launch display

cd ..

epiphany SlideShow.html & PID=$! # & sleep 10
# xte "key F11" -x:0 & sleep 10  # This literally to pushes the F11 key
# xte "str  "                    # And this literally pushes space
sleep $DISPLAYTIME; kill $PID
