import glob
import os

for file in glob.glob("../img/*"):
    os.remove(file)
