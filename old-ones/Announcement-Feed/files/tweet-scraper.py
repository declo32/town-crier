#!/usr/bin/python

import time

import twitter

import utils

# OAuth twitter thing
print("Logging into Twitter")
api = twitter.Api(consumer_key="UH7Eh6flT8snkSfn7NlsxOhkk",
                  consumer_secret="Oskfr9Ime0H8NSKb0VVpMmHHbKEPYfitgwmHMUuECGV6u52jg3",
                  access_token_key="399061958-wFMQT9UVxr4YD1lsrHvE7U1HGwreTxebDl9mgFP5",
                  access_token_secret="PfBTY8mmikkshNVRHxZyC4uTbbebBqFIOryWoUeJQ8RPH")


# A file containing a list of usernames from which to scrape tweets
print("Finding usernames")
username_file = open(utils.USERNAMES_PATH, "r")
username_list = [line
                 .replace("\n", "")                     # No new lines
                 for line in username_file.readlines()
                 if line and "#" not in line]           # Leave out blank lines and comments


# Format data to be added to feed.pkl file
feed_data = []

current_time = int(time.time())  # Don't want old stuff
SECONDS_PER_WEEK = 604800

for user in username_list:
    print("Gathering data for \033[94m @%s \033[0m" % user)

    try:
        statuses = api.GetUserTimeline(screen_name=user)
    except twitter.error.TwitterError:
        print("Data for \033[94m @%s \033[0m could not be retrieved" % user)
        continue

    for status in statuses[:3]:  # 3 most recent
        if (current_time - status.created_at_in_seconds) <= SECONDS_PER_WEEK and "RT" not in status.text:
            feed_datum = utils.Announcement(header=user,
                                            text=(status.text
                                                  .replace("\n", " ")         # No new lines
                                                  .encode("ASCII", "ignore")  # Only ASCII characters
                                                  .decode("UTF-8")),          # str, not bytes
                                            source="Twitter")
            feed_data.append(feed_datum)


# Add formatted data to feed.pkl file
utils.append_feed(feed_data)
