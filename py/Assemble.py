import sys
import os

path = sys.argv[1]

with open(path + "html/Skeleton.html", "r", errors="ignore") as file:
    skeleton = file.read()

with open(path + "html/from-school.html", "r", errors="ignore") as file:
    from_school = file.read()

with open(path + "html/from-twitter.html", "r", errors="ignore") as file:
    from_twitter = file.read()

with open(path + "SlideShow.html", "w") as file:
    file.write(
        skeleton.format(FROM_SCHOOL=from_school, FROM_TWITTER=from_twitter)
    )
