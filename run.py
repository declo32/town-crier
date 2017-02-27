import os

os.chdir("py")


def run(program):
    print("Running {program}".format(program=program))
    os.system("python " + program)

# run("Announcement-Scrape.py")
run("Twitter-Scrape.py")
run("Assemble.py")
