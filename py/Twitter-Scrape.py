import twitter

import TwitterAPIOAuth as TOAuth  # Local

api = twitter.Api(consumer_key=TOAuth.CONSUMER_KEY,
                  consumer_secret=TOAuth.CONSUMER_SECRET,
                  access_token_key=TOAuth.ACCESS_TOKEN_KEY,
                  access_token_secret=TOAuth.ACCESS_TOKEN_SECRET)

# Get all registered usernames
users_file = open("../users.txt", "r")
usernames = users_file.read().splitlines()  # Take each line without getting a newline character
users_file.close()

# Get all valid users
users = []
for username in usernames:
    try:
        users.append(
            api.GetUser(screen_name=username)
        )
    except twitter.error.TwitterError:
        print("User {username} not found".format(username=username))

# Format tweets

tweets = [
    """
    <img class="profile-pic" src="{profile_pic_url}"></img>
    <h1 class="user">{user}</h1>
    <h3 class="message">{message}</h3>
    <img class="tweet-image" src="{img_url}"></img>
    <br>
    """.format(profile_pic_url=user.profile_image_url,
               user=user.screen_name,
               message="Hello, World!",
               img_url="")
    for user in users
]
