#!/usr/bin/env bash

# Parse arguments

DISPLAYTIME=infinity
USEOLD=false
SHUTDOWN=false
for i in "$@"; do
	case $i in
		-t=*|--display-time=*)
		DISPLAYTIME="${i#*=}"
		shift
		;;
		
		-u|--use-old)
		USEOLD=true
		shift
		;;
		
		-s|--shutdown)
		SHUTDOWN=true
		shift
		;;
		
		-h|--help)
		echo "-t or --display-time to set display time
-u or --use-old      to use old html
-s or --shutdown     to shutdown afterwards"
		exit 0
		;;
	esac
done

echo "DISPLAYTIME = ${DISPLAYTIME}"
echo "USEOLD      = ${USEOLD}"
echo "SHUTDOWN    = ${SHUTDOWN}"

# Get info

if [ ! $USEOLD = true ]; then
	cd py
	
	declare -a FILES=("Announcement-Scrape.py" "Twitter-Scrape.py" "Assemble.py")
	for FILENAME in "${FILES[@]}"
	do
		echo "Running $FILENAME"
		python3 $FILENAME
	done
	
	cd ..
fi

# Launch display

unclutter -display :0 -noevents -grab & PID1=$!  # This hides the mouse
epiphany SlideShow.html & PID2=$!
sleep 20; xte "key F11" -x:0  # This literally to pushes the F11 key
sleep $DISPLAYTIME
echo "I'm about to kill the processes known as ${PID1} and ${PID2}"
kill $PID1
kill $PID2

# Shutdown

if [ $SHUTDOWN = true ]; then
	shutdown --poweroff now
fi
