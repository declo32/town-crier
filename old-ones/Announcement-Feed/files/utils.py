#!/usr/bin/python

"""General utilities: functions/variables that we use a lot"""

import os
import pickle

PROJECT_PATH = os.getcwd()

# Ordered alphabetically
FEED_PATH = PROJECT_PATH + "/files/feed.pkl"
LOGO_PATH = PROJECT_PATH + "/files/static/logo.jpg"
OPTIONS_PATH = PROJECT_PATH + "/options/"
PICTURES_PATH = PROJECT_PATH + "/files/pictures/"
USERNAMES_PATH = PROJECT_PATH + "/options/usernames.txt"


def get_feed():
    feed_file = open(FEED_PATH, "rb")
    feed = pickle.load(feed_file)
    feed_file.close()

    return feed


def set_feed(feed_data):
    feed_file = open(FEED_PATH, "wb")
    pickle.dump(feed_data, feed_file)
    feed_file.close()


def append_feed(feed_data):
    feed = get_feed()
    feed += feed_data
    set_feed(feed)


class Announcement:

    def __init__(self, header, text, source, picture=None):
        self.header = header
        self.text = text
        self.source = source
        self.picture = picture
        self.display_time = self.time_text()

    def __str__(self):
        return "%s - %s" % (self.source, self.header)

    def time_text(self, time_per_word=250):

        if "You need JavaScript enabled to view it" in self.text:
            return 100

        word_amount = len(self.text.split(" "))

        if word_amount < 10:
            return 2 * word_amount * time_per_word
        else:
            return word_amount * time_per_word
