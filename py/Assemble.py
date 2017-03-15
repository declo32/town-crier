with open("../html/Skeleton.html", "r", errors="ignore") as file:
    skeleton = file.read()

with open("../html/from-school.html", "r", errors="ignore") as file:
    from_school = file.read()

with open("../html/from-twitter.html", "r", errors="ignore") as file:
    from_twitter = file.read()

with open("../SlideShow.html", "w") as file:
    file.write(
        # I don't like this
        skeleton % (from_school, from_twitter)
    )
