"""
Takes the announcements from the school website, by
    - Going to a list of links to all announcements, ever
    - Getting the first link in that list, to the most recent announcements
    - Opening that link and finding the html containing the announcements
    - Print out that html
"""

import re
import urllib.request

from bs4 import BeautifulSoup

school_base_url = "http://www.scituate.k12.ma.us"

# Get the "Announcements Archive" page of the SHS website
school_archive_url = school_base_url + "/index.php/about-shs/daily-announcements-archive"
archive_request = urllib.request.Request(school_archive_url)        # Request website
archive_response = urllib.request.urlopen(archive_request)          # Get response
archive_data = archive_response.read()                              # Get website's html
archive_soup = BeautifulSoup(archive_data, "lxml")                  # Convert html to BeautifulSoup object

# Find link to current announcements
table = archive_soup.find("table")                                   # Table of announcements
table_body = table.find("tbody")
rows = table_body.find_all("tr")                                     # All elements of table
announcements_url = school_base_url + rows[0].find("a").get("href")  # Finds the link inside the first row

# Get the current announcement page
announcements_request = urllib.request.Request(announcements_url)       # Request website
announcements_response = urllib.request.urlopen(announcements_request)  # Get response
announcements_data = announcements_response.read()                      # Get website's html
announcements_soup = BeautifulSoup(announcements_data, "lxml")          # Convert html to BeautifulSoup object
announcements_final = announcements_soup.find("div", attrs={"itemprop": "articleBody"})

# Make it better
url_re = re.compile(r"https?://.*", re.I)
for img in announcements_final.find_all("img"):       # Fix relative links
    if not url_re.match(img["src"]):
        print(img["src"])
        img["src"] = announcements_url + img["src"]
announcements_final = announcements_final.prettify()  # To make it a string, not for aesthetics

with open("../html/from-school.html", "w") as file:
    file.write(announcements_final)
