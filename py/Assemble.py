with open("../html/Skeleton.html", "rb", errors="replace") as file:
    skeleton = file.read()

with open("../html/from-school.html", "rb", errors="replace") as file:
    from_school = file.read()

with open("../html/from-twitter.html", "rb", errors="replace") as file:
    from_twitter = file.read()

with open("../SlideShow.html", "wb") as file:
    file.write(
        # I don't like this
        skeleton % (from_school, from_twitter)
    )
