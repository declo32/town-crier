#!/usr/bin/env bash

# Parse arguments

TIMEOUT=$(expr 60*60*8)  # Defaults to 8 hours
for i in "$@"; do
	case $i in
		--run-time=*)
		RUNTIME="${i#*=}"
		shift
		;;
		
		*)
		echo "$i isn't a thing"
	esac
done

echo "RUNTIME = ${RUNTIME}"

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

epiphany SlideShow.html & PID=$! & sleep 10
xte "key F11" -x:0  # This literally pretends to push the F11 key
sleep $TIMEOUT; kill $PID
