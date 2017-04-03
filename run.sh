#!/usr/bin/env bash

# Parse arguments

TIMEOUT=$(expr 60*60*8)  # Defaults to 8 hours
for i in "$@"; do
	case $i in
		--time-out=*)
		TIMEOUT="${i#*=}"
		shift
		;;
		
		*)
		echo "$i isn't a thing"
	esac
done

echo "TIMEOUT = ${TIMEOUT}"

# Get info

cd py

# Order is important
declare -a files=(
    "Announcement-Scrape.py"
    "Twitter-Scrape.py"
    "Assemble.py"
)

for file in "${files[@]}"; do  # files[@]
    echo "Running ${file}"
    sudo python3 "${file}"
done

# Launch display

cd ..

epiphany SlideShow.html & PID=$!; sleep $TIMEOUT; kill $PID
