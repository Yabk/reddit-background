#!/usr/bin/python3

import sys
import os
import shutil
import random
import subprocess
import re
import requests

"""Downloads an image from one of subreddits listed in file
subreddits.txt and sets it as a background image"""

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def getsub():
    """Returns url to a random subreddit from subreddits.txt"""

    f = open(__location__ + '/subreddits.txt', 'r')
    text = f.read()
    f.close()

    subreddits = text.split('\n')
    if subreddits[-1] == '':
        subreddits.pop(-1)

    sub = random.choice(subreddits)

    print(sub)

    return 'https://www.reddit.com' + sub

def getimgurl(sub):
    """Returns an image url from top post on given sub"""

    response = requests.get(url = sub+'top/.json', headers = {'User-agent': 'reddit-background.bot'})
    data = response.json()

    try:
        posts = data['data']['children']
    except KeyError:
        print("Too many requests!\nTry again later.")
        sys.exit(1)

    for i in range (len(posts)):
        url = posts[i]['data']['url']
        if (re.search(r'\.jpg', url)):
            return url

    return

def setbackground(image):
    """Sets image.jpg as background image"""

    cmd = 'gsettings set org.gnome.desktop.background picture-uri file://' + os.path.abspath(image)

    subprocess.call(cmd.split())

    return

def main():
    sub = getsub()
    url = getimgurl(sub)
    print(url)

    #Downloading image from the url
    response = requests.get(url, stream=True)
    with open(__location__ + '/image.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    setbackground(__location__ + '/image.jpg')

if __name__ == '__main__':
    main()
