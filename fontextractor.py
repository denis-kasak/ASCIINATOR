import math
import os

import cv2

skindir = "./res/charfilter/all/"


def setskin(skin):
    global skindir
    skindir = "./res/charfilter/" + skin + "/"


def sortfonts(color):
    charlist = createcolor(color[0], color[1])

    minv = 1000
    maxv = 0

    # find the most/the least bright character
    for i in range(len(charlist[0])):
        if charlist[0][i] < minv:
            minv = charlist[0][i]
        elif charlist[0][i] > maxv:
            maxv = charlist[0][i]

    # load images in list
    for i in range(len(charlist[1])):
        charlist[1][i][0] = 256 * ((charlist[1][i][0] - minv) / (maxv - minv))
        charlist[0][i] = charlist[1][i][0]

    charlist[0] = sorted(charlist[0])
    charlist[1] = sorted(charlist[1])

    for i in range(len(charlist[1])):
        charlist[1][i][1] = cv2.imread(charlist[1][i][1])

    w = 20
    h = 32

    return [w, h, charlist]


def getskins():
    liste = [x[0] for x in os.walk("./res/charfilter/")]
    skins = []
    for i in range(len(liste)):
        if i == 0:
            continue
        else:
            skins.append(liste[i].replace("./res/charfilter/", ""))

    return skins


def createcolor(fontbgr, bgbgr):
    charlist = [[], []]
    indeximg = 0
    while os.path.isfile(skindir + f'{indeximg}.jpg'):
        path = skindir + f'{indeximg}.jpg'
        img = cv2.imread(path)
        h = img.shape[0]
        w = img.shape[1]

        avgimg = 0

        for x in range(0, w):
            for y in range(0, h):
                px = img[y, x]
                avgimg += (sum(px)) / 3

                avgpx = sum(px) / len(px)
                fontopac = avgpx
                bgopac = 255 - fontopac
                fontopac = fontopac / 256
                bgopac = bgopac / 256
                img[y, x][0] = math.floor(fontbgr[0] * fontopac + bgbgr[0] * bgopac)
                img[y, x][1] = math.floor(fontbgr[1] * fontopac + bgbgr[1] * bgopac)
                img[y, x][2] = math.floor(fontbgr[2] * fontopac + bgbgr[2] * bgopac)

        path = f'./temp/chars/{indeximg}.jpg'
        cv2.imwrite(path, img)

        avgimg = (avgimg / ((w - 1) * (h - 1)))
        charlist[0].append(avgimg)
        charlist[1].append([avgimg, path])
        indeximg = indeximg + 1

    return charlist


if __name__ == '__main__':
    # createchars()
    # sortfonts()
    print(getskins())
