#!/usr/bin/python3

import sys
import os
import shutil
import random
import subprocess
import re
import requests
import struct
import imghdr

"""Downloads an image from one of subreddits listed in file
subreddits.txt and sets it as a background image"""

__location__ = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))

def getsubs():
    """Returns url to a random subreddit from subreddits.txt"""

    f = open(__location__ + '/subreddits.txt', 'r')
    text = f.read()
    f.close()

    subreddits = text.split('\n')
    if subreddits[-1] == '':
        subreddits.pop(-1)

    random.shuffle(subreddits)
    return subreddits

def getimg(sub, todir):
    """Downloads and image from top post on given sub"""

    try:
        response = requests.get(url = sub+'top/.json', headers = {'User-agent': 'reddit-background.bot'})
    except requests.exceptions.ConnectionError:
        print(sub)
        print('No connection')
        sys.exit(1)

    data = response.json()

    try:
        posts = data['data']['children']
    except KeyError:
        print("Too many requests!\nTry again later.")
        sys.exit(1)

    for i in range (len(posts)):
        url = posts[i]['data']['url']
        match = re.search(r'\.jpg|\.png', url)
        if (match):
            ext = match.group()
            #Downloading image from the url
            response = requests.get(url, stream=True)
            with open(__location__ + '/tmp' + ext, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            size = get_image_size(__location__ + '/tmp' + ext)
            if (size):
                (width, height) = size
            else:
                continue
            print(url)
            print('width:  ' + str(width))
            print('height: ' + str(height))
            if width >= 1920 and height >= 1080:
                os.rename(__location__ + '/tmp' + ext, __location__ + '/image' + ext)

                if todir:
                    todir = os.path.abspath(todir)
                    if not os.path.isdir(todir):
                        os.makedirs(todir)

                    imgname = re.search(r'/\w+'+ext, url).group()
                    shutil.copyfile(__location__ + '/image' + ext, todir + imgname)
                return __location__ + '/image' + ext
    return

def setbackground(image):
    """Sets image.jpg as background image"""

    cmdBackground = 'gsettings set org.gnome.desktop.background picture-uri file:' + os.path.abspath(image)
    cmdScreensaver = 'gsettings set org.gnome.desktop.screensaver picture-uri file:' + os.path.abspath(image)

    os.system(cmdBackground)
    os.system(cmdScreensaver)

    return

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg' or re.search(r'.jpg', fname):
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height

def main():
    args = sys.argv[1:]
    todir = None

    if args:
        if args[0] == '--help' or args[0] == '-h':
            print('redditback - downloads top image from random subreddit listed in subreddits.txt\n')
            print('Usage: [--todir|-o dir]')
            sys.exit()
        elif args[0] == '--todir' or args[0] == '-o':
            todir = args[1]
        else:
            print('Usage: [--todir|-o dir]')
            sys.exit()

    subs = getsubs()
    while subs:
        sub = subs.pop(0)
        print(sub)
        img = getimg('https://www.reddit.com' + sub, todir)
        if img:
            print('OK')
            setbackground(img)
            break
        elif not subs:
            print("Could not retrieve any images from given subreddits.")

if __name__ == '__main__':
    main()
