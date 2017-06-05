#!/usr/bin/python

import glob
import os

import utils

for pic in glob.glob(utils.PICTURES_PATH + "*"):  # Remove pictures
    print("Deleting %s" % pic)
    os.remove(pic)

print("Resetting %s" % utils.FEED_PATH)
utils.set_feed([])  # Reset feed.pkl
