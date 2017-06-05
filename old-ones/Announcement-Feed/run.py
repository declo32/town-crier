#!/usr/bin/python

import os
import time
import sys

INTERVAL = 7 if "-present" in sys.argv else 0
PYTHON = "python"  # How to execute programs in /files/ (python FILENAME)


def execute(message, filepath):
    """prints the "message" parameter, then executes a file as defined in the "filepath" parameter"""
    print("\033[95m" + message + "\033[0m")
    time.sleep(INTERVAL)
    os.system(PYTHON + " " + filepath)
    print("\033[92m" + "Done!" + "\033[0m")
    print()

# the entire process(scraping, writing, collecting, display, etc.) will be executed every {interval} seconds.
# interval=100 deprecated: now replaced by the open_for variable in display.py
while True:
    # Do whatever you need to do in here, this will replicate the run.sh process.
    try:
        execute("Resetting files...",                                "files/reset.py")
        execute("Scraping the Scituate High School website...",      "files/web-scraper.py")
        execute("Scraping the tweets from the list of usernames...", "files/tweet-scraper.py")
        execute("Downloading the pictures from certain tweets...",   "files/picture_getter.py")
        execute("Launching display...",                              "files/display.py")

        latest_refresh = time.strftime("%I:%M:%S on %m/%d/%Y")
        print("Latest refresh was at " + latest_refresh)
        time.sleep(3)
    # Stops CTRL-C from throwing crazy errors
    except KeyboardInterrupt:
        print("\nStopping...")
        latest_refresh = time.strftime("%I:%M:%S on %m/%d/%Y")
        print("Stopped at " + latest_refresh)
        break
