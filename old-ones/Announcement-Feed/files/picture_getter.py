#!/usr/bin/python

"""
read through feed.pkl and find all those "https://t.co" links, turn them into urls,
and download them into a directory called "pictures"
"""

import urllib.request
import requests
import re

from bs4 import BeautifulSoup

import utils

feed = utils.get_feed()


link_pattern = re.compile(r"https://t\.co/[\da-zA-Z]{10}")

for announcement in feed:
    text = announcement.text
    link = re.findall(link_pattern, text)

    if link:

        print()  # A E S T H E T I C

        link = link[0]  # Only expecting one link

        announcement.text = announcement.text.replace(link, "")  # Get rid of link from text

        # Find the picture
        print("Finding picture for \033[94m %s \033[0m" % link)
        site_request = requests.get(link)             # Get website
        site_data = site_request.text                 # Get website's html
        site_soup = BeautifulSoup(site_data, "lxml")  # Convert html to BeautifulSoup object

        try:                                          # Could link to a video or something: we don't want that
            picture_link = (site_soup
                            .find("div", "AdaptiveMedia-singlePhoto")
                            .find("img")
                            .get("src"))
        except AttributeError:
            print("\033[94m %s \033[0m doesn't link to a picture." % link)
            continue

        # Download the picture
        print("Downloading picture for \033[94m %s \033[0m" % link)
        picture_req = urllib.request.Request(picture_link)
        picture_resp = urllib.request.urlopen(picture_req)
        picture_data = picture_resp.read()

        picture_path = utils.PICTURES_PATH + link[13:]  # Create a unique filename based on url
        picture_file = open(picture_path, "wb")
        picture_file.write(picture_data)
        picture_file.close()

        announcement.picture = picture_path

# Update feed
utils.set_feed(feed)
