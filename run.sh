#!/usr/bin/env bash

# Parse arguments

DISPLAYTIME=28800
for i in "$@"; do
	case $i in
		-d=*|--display-time=*)
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

epiphany SlideShow.html & PID=$!
sleep 10; xte "key F11" -x:0  # This literally to pushes the F11 key
sleep $DISPLAYTIME
echo "I'm about to kill the process known as ${PID}"
kill $PID
