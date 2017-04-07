#!/usr/bin/env bash

# Parse arguments

DISPLAYTIME=28800
USEOLD=false
for i in "$@"; do
	case $i in
		-d=*|--display-time=*)
		DISPLAYTIME="${i#*=}"
		shift
		;;
		
		-u|--use-old)
		USEOLD=true
		shift
		;;
		
		-h|--help)
		echo "-d or --display-time to set display time
-u or --use-old      to use old html"
		exit 0
		;;
	esac
done

echo "DISPLAYTIME = ${DISPLAYTIME}"
echo "USEOLD      = ${USEOLD}"

# Get info

if [ !$USEOLD ]; then
	echo "YOU DIDN'T USE OLD"
	cd py
	
	python3 Announcement-Scrape.py
	python3 Twitter-Scrape.py
	python3 Assemble.py
	
	cd ..
	
else
	echo "YOU DID USE OLD"
fi

# Launch display

epiphany SlideShow.html & PID=$!
sleep 10; xte "key F11" -x:0  # This literally to pushes the F11 key
sleep $DISPLAYTIME
echo "I'm about to kill the process known as ${PID}"
kill $PID
