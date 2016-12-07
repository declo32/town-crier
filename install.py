#this file is used to do all the npm installations, gem installations, and any other setup that is needed to run Town Crier seemlessly
from os import system

gems = ["mechanize", "nokogiri", "open-uri", "json", "twitter"]

for g in gems:
    system("sudo gem install "+g)
