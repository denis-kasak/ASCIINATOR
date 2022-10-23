import csv
import os
import shutil

import cv2

skindir = "./res/charfilter/all/"


def setskin(skin):
    global skindir
    if skindir == "./res/charfilter/all":
        skindir = ""
    skindir = "./res/charfilter/" + skin + "/"


def sortfonts():
    i = 0
    charlist = []
    while os.path.isfile(skindir + f'{i}.jpg'):
        path = skindir + f'{i}.jpg'
        img = cv2.imread(path)
        h = img.shape[0]
        w = img.shape[1]

        avg = 0

        for x in range(0, w):
            for y in range(0, h):
                px = img[y, x]
                avg += (sum(px)) / 3
        avg = avg / ((w - 1) * (h - 1))
        charlist.append([avg, path])
        i = i + 1

    charlist = sorted(charlist)

    minv = 1000
    maxv = 0
    for i in range(len(charlist)):
        if charlist[i][0] < minv:
            minv = charlist[i][0]
        elif charlist[i][0] > maxv:
            maxv = charlist[i][0]
    for i in range(len(charlist)):
        charlist[i][0] = (charlist[i][0] - minv) / (maxv - minv)
        charlist[i][1] = cv2.imread(charlist[i][1])

    w = 20
    h = 32
    return [w, h, charlist]


def getskins():
    list = [x[0] for x in os.walk("./res/charfilter/")]
    skins = []
    for i in range(len(list)):
        if i == 0:
            continue
        else:
            skins.append(list[i].replace("./res/charfilter/", ""))

    return skins


if __name__ == '__main__':
    # createchars()
    # sortfonts()
    print(getskins())
