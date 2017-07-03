#!/usr/bin/python

import os
import urllib
import random
import json
import commands

"""Downloads an image from one of subreddits listed in file
subreddits.txt and sets it as a background image"""

def getsub():
    """Returns url to a random subreddit from subreddits.txt"""

    f = open('subreddits.txt', 'r')
    text = f.read()
    f.close()

    subreddits = text.split('\n')
    if subreddits[-1] == '':
        subreddits.pop(-1)

    return 'https://www.reddit.com' + random.choice(subreddits)

def getimgurl(sub):
    """Returns an image url from hottest post on given sub"""

    f = urllib.urlopen(sub+'hot/.json')
    text = f.read()
    data = json.loads(text)

    return data['data']['children'][1]['data']['url']


def setbackground(image):
    """Sets image.jpg as background image"""

    cmd = 'gsettings set org.gnome.desktop.background picture-uri file://' + os.path.abspath(image)

    commands.getstatusoutput(cmd)

    return

def main():
    sub = getsub()
    urllib.urlretrieve(getimgurl(sub), 'image.jpg')

    setbackground('image.jpg')

if __name__ == '__main__':
    main()
