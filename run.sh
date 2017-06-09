#!/usr/bin/env bash

cd ~/town-crier/

# Do title

echo "__                                      _           "
echo "| |_ _____      ___ __         ___ _ __(_) ___ _ __ "
echo "| __/ _ \ \ /\ / / '_ \ _____ / __| '__| |/ _ \ '__|"
echo "| || (_) \ V  V /| | | |_____| (__| |  | |  __/ |   "
echo " \__\___/ \_/\_/ |_| |_|      \___|_|  |_|\___|_|   "
echo ""

# Parse arguments

TCPATH="/home/pi/town-crier/"
for i in "$@"; do
	case $i in
		-p=*|--path=*)
		TCPATH="${i#*=}"
		shift
		;;
	esac
done

# Get info

declare -a FILES=("Announcement-Scrape.py" "Twitter-Scrape.py" "Assemble.py")
for FILENAME in "${FILES[@]}"
do
	echo "Running ${FILENAME}"
	python3 "${TCPATH}${FILENAME}"
done
