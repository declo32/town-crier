import sys
import os
import re

path = os.path.split(sys.argv[0])[0]

users = [
    ("JohnDoe", "http://leafii.com/images/defaultProfilePic.png",
     ["I enjoy doing human things, like digesting nutrients taken from food.",
      "MOHAMBOT ALI RENDERS JOE FRAZIER USELESS (COLORIZED 1974) https://i.redd.it/ch9cm6uvluty.jpg",
      "YUMMY.EXE SPAGHETTI https://i.redditmedia.com/poiEHofB3Il7aY2sLaCILdGvY4eGytASwEqS6iUvrqM.jpg?w=432&s=0ae5e6249dcbdd0fb77b14fa64e0b0ae"]),

    ("KenM", "https://pbs.twimg.com/profile_images/1641005897/horseyavatar_400x400.jpg",
     ["here's an idea: if you're not responsible enough to take care of yourself, DON'T have grandchildren",
      "would be fun to spend a day with the chickens, dancing and playing the fool",
      "one questions the wisdom of allowing more planets into the system when our resources are limited enough as it is"]),

    ("ABoat", "http://assets.academy.com/mgen/26/10003026.jpg?is=500,500",
     ["I AM A BOAT http://clipartix.com/wp-content/uploads/2016/04/Sport-fishing-boat-clip-art-free-clipart-images-2-clipartcow.png",
      "IK BEN EEN BOOT http://www.boatkits.eu/images/mod/mod-3.jpg",
      "IS BÀD ME http://www.irishboats.com/clinkerbuilt/clinkerbuiltpunt.jpg"])
]

tweet_re = re.compile(r"^(?P<message>.*?)\s*(?P<image_url>https?://.*)?$", re.X)
tweets_html = ""

with open(path + "/../html/twitter-skeleton.html") as file:
    template = file.read()

    for un, pic, tl in users:
        for raw_tweet in tl:
            tweet = tweet_re.match(raw_tweet)

            if tweet:
                if tweet.group("image_url"):
                    img_tag = "<img src={pic}>".format(pic=tweet.group("image_url"))
                    tweets_html += template.format(
                        PROFILE_PIC=pic,
                        USERNAME=un,
                        MESSAGE=tweet.group("message"),
                        IMAGE_URL=img_tag
                    )
                else:
                    tweets_html += template.format(
                        PROFILE_PIC=pic,
                        USERNAME=un,
                        MESSAGE=tweet.group("message"),
                        IMAGE_URL="",
                    )

tweets_html = tweets_html.encode("UTF-8")

with open(path + "/../html/from-twitter.html", "wb") as file:
    file.write(tweets_html)
