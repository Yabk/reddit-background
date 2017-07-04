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

    response = requests.get(url = sub+'top/.json')
    data = response.json()

    try:
        posts = data['data']['children']
    except KeyError:
        print("Too many requests!\nTry again later.")
        sys.exit(1)

    for i in range (1, len(posts)):
        url = posts[i]['data']['url']
        if (re.search(r'\.img', url)):
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
    with open('image.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    setbackground('image.jpg')

if __name__ == '__main__':
    main()
