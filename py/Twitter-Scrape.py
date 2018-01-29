import sys
import os
import time
import re
import urllib.request
import http.client

import twitter
from bs4 import BeautifulSoup

import TwitterAPIOAuth as TOAuth  # Local. Get your own, hippy.

path = sys.argv[1]  # Give name as command-line argument


def get_img_url(tco_url):
    # OH MY GOD I'M SORRY
    
    if tco_url is None:
        return ""
    
    try:
        req = urllib.request.Request(tco_url)
        resp = urllib.request.urlopen(req)
        soup = BeautifulSoup(resp, "lxml")
    except http.client.IncompleteRead:
        print("It didn't work")
        return ""
    except Exception as e:
        print(e)
        print("Something happened that I didn't plan for... It should be fine.")
    else:
        try:
            return soup.find("div", attrs={"class": "AdaptiveMedia-photoContainer js-adaptive-photo "}).find("img")
        except AttributeError:  # Doesn't link to an image
            return ""

# These are from a local file
api = twitter.Api(consumer_key=TOAuth.CONSUMER_KEY,
                  consumer_secret=TOAuth.CONSUMER_SECRET,
                  access_token_key=TOAuth.ACCESS_TOKEN_KEY,
                  access_token_secret=TOAuth.ACCESS_TOKEN_SECRET)

# Get all registered usernames
with open(path + "users.txt", "r") as users_file:
    usernames = [username
                 for username in users_file.read().splitlines()  # Take each line without getting a newline character
                 if "#" not in username]                         # For comments

# Get all valid users' recent posts
users = []
current_time = time.time()
limit_in_seconds = 60 * 60 * 24 * 7  # One week
for username in usernames:
    print("Finding {username}".format(username=username))
    try:
        users.append(
            (
                username,
                [x for x in api.GetUserTimeline(screen_name=username)
                 if current_time - x.created_at_in_seconds <= limit_in_seconds]
            )
        )
    except twitter.error.TwitterError:
        print("User {username} not found".format(username=username))

# Format tweets
tweet_re = re.compile(r"^(?P<message>.*?)\s*(?P<image_url>https?://t\.co/\w+)?$", re.X)
tweets_html = ""

with open(path + "html/twitter-skeleton.html") as file:
    template = file.read()

    for un, tl in users:  # username, tweet list
        for raw_tweet in tl:
            tweet = tweet_re.match(raw_tweet.text)

            if tweet:
                tweets_html += template.format(
                    PROFILE_PIC=raw_tweet.user.profile_image_url,
                    USERNAME=un,
                    MESSAGE=tweet.group("message"),
                    IMAGE_URL=get_img_url(tweet.group("image_url")),
                )

tweets_html = tweets_html.encode("UTF-8")  # Weird characters, some map to <undefined>

with open(path + "html/from-twitter.html", "wb") as file:
    file.write(tweets_html)
