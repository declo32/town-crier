skeleton_file = open("../html/Skeleton.html", "rb")
skeleton = skeleton_file.read()
skeleton_file.close()

from_school_file = open("../html/from-school.html", "rb")
from_school = from_school_file.read()
from_school_file.close()

from_twitter_file = open("../html/from-twitter.html", "rb")
from_twitter = from_twitter_file.read()
from_twitter_file.close()

with open("../SlideShow.html", "wb") as file:
    file.write(
        # I don't like this
        skeleton % (
            from_school,
            from_twitter,
        )
    )
