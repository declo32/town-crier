import time

import twitter

import TwitterAPIOAuth as TOAuth  # Local, get your own

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
# TODO Figure out how to get image from tweet
tweets = "\n".join([
    """
    <img class="profile-pic" src="{tweet.user.profile_image_url}"></img>
    <h1 class="user">{username}</h1>
    <h3 class="message">{tweet.text}</h3>
    <img class="tweet-image" src="{tweet.img]}"></img>
    <br>
    """.format(username=user[0], tweet=tweet)

    for user in users
    for tweet in user[1]
    ]).encode("UTF-8")  # Get rid of uncool characters

with open("../html/from-twitter.html", "wb") as file:
    file.write(tweets)
