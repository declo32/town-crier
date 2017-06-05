#!/usr/bin/python

import requests
import itertools

from bs4 import BeautifulSoup

import utils

print("Finding most recent announcements")


# Gets the "Announcements Archive" page of the SHS website
url = "http://www.scituate.k12.ma.us/index.php/about-shs/daily-announcements-archive"
archive_request = requests.get(url)                 # Get website
archive_data = archive_request.text                 # Get website's html
archive_soup = BeautifulSoup(archive_data, "lxml")  # Convert html to BeautifulSoup object


# Finds the table of all announcements
table = archive_soup.find("table")   # Table of announcements
table_body = table.find("tbody")
rows = table_body.find_all("tr")
ele = rows[0].find("a").get("href")  # Finds the link inside the first row (to most recent announcements)


# Gets the most recent announcements page of the SHS website
announcement_url = url + ele
announcement_request = requests.get(announcement_url)         # Get website
announcement_data = announcement_request.text                 # Get website's html
announcement_soup = BeautifulSoup(announcement_data, "lxml")  # Convert html to BeautifulSoup object
announcement_list = announcement_soup.find_all("p")[2:]       # Get all announcements (in <p> tags)


print("Reading announcements")


# Take all ASCII text from announcement_list and group together announcements
# This is my least favorite part. There's probably a more Pythonic way to do this.
announcement_text = [announcement.text
                     .replace("\n", "")          # No new lines
                     .encode("ASCII", "ignore")  # Only take the ASCII characters, ignore the rest
                     .decode("UTF-8")            # Turns it into a str

                     for announcement in announcement_list]

announcement_text = list(filter(None, announcement_text))  # No empty strings
announcement_text = ["\n".join(grp)                        # Group together announcements
                     for key, grp in itertools.groupby(announcement_text, '*****'.__eq__)
                     if not key]


print("Writing announcements to a file")


# Save announcements to a file
feed_data = [
    utils.Announcement(header="School",
                       text=text,
                       source="SHS Announcement Website")
    for text in announcement_text
]

utils.append_feed(feed_data)
