import time
import re
import urllib.request

import twitter
from bs4 import BeautifulSoup

import TwitterAPIOAuth as TOAuth  # Local. Get your own, hippy.


def get_img_url(tco_url):
    req = urllib.request.Request(tco_url)
    resp = urllib.request.urlopen(req)
    soup = BeautifulSoup(resp)

    try:
        img_url = soup.find("div", attrs={"class": "AdaptiveMedia-photoContainer js-adaptive-photo "}).find("img")
        return soup.find("div", attrs={"class": "AdaptiveMedia-photoContainer js-adaptive-photo "}).find("img")
    except AttributeError:
        # Doesn't link to an image
        return ""

api = twitter.Api(consumer_key=TOAuth.CONSUMER_KEY,
                  consumer_secret=TOAuth.CONSUMER_SECRET,
                  access_token_key=TOAuth.ACCESS_TOKEN_KEY,
                  access_token_secret=TOAuth.ACCESS_TOKEN_SECRET)

# Get all registered usernames
users_file = open("../users.txt", "r")
usernames = users_file.read().splitlines()  # Take each line without getting a newline character
users_file.close()

# Get all valid users' recent posts
users = []
current_time = time.time()
limit_in_seconds = 60 * 60 * 24 * 7  # One week
for username in usernames:
    try:
        user = (
            username,
            [x for x in api.GetUserTimeline(screen_name=username)
             if current_time - x.created_at_in_seconds <= limit_in_seconds]
        )
        users.append(user)
    except twitter.error.TwitterError:
        print("User {username} not found".format(username=username))

# Format tweets
tweet_re = re.compile(r"^(?P<message>.*?)\s*(?P<image_url>https://t\.co/\w+)?$", re.X)
tweets_html = ""

with open("../html/twitter-skeleton.html") as file:
    template = file.read()

    for un, tl in users:
        for raw_tweet in tl:
            tweet = tweet_re.match(raw_tweet.text)

            if tweet:
                if tweet.group("image_url"):
                    tweets_html += template.format(
                        PROFILE_PIC=raw_tweet.user.profile_image_url,
                        USERNAME=un,
                        MESSAGE=tweet.group("message"),
                        IMAGE_URL=get_img_url(tweet.group("image_url")),
                    )
                else:
                    tweets_html += template.format(
                        PROFILE_PIC=raw_tweet.user.profile_image_url,
                        USERNAME=un,
                        MESSAGE=tweet.group("message"),
                        IMAGE_URL="",
                    )

tweets_html = tweets_html.encode("UTF-8")

with open("../html/from-twitter.html", "wb") as file:
    file.write(tweets_html)
