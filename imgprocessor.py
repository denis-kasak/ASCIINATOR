import math
import multiprocessing
import os
from multiprocessing import Process
import cv2
import time
import util
from fontextractor import sortfonts
from bisect import bisect_left
import numpy


def img2ascii(img, indeximg, charlist, charsize):
    charw = charsize[0]
    charh = charsize[1]

    charlist = charlist[2]

    h = img.shape[0]
    w = img.shape[1]

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for y in range(0, h, charh):
        for x in range(0, w, charw):
            avg = numpy.sum(img[y:y + charh, x:x + charw])

            avg = avg / (charw * charh * 3)
            i_closest = bisect_left(charlist[0], avg)
            char = charlist[1][i_closest][1]
            img[y:y + charh, x:x + charw] = cv2.resize(char, [charw, charh])

    cv2.imwrite(f'./temp/frames_out/{indeximg}.jpg', img)


def singleframe(color, res, img):
    charlist = sortfonts(color)

    charw = math.floor(charlist[0] // res)
    charh = math.floor(charlist[1] // res)

    img2ascii(img, 0, charlist, [charw, charh])

    img = cv2.imread("./temp/frames_out/0.jpg")

    cv2.imshow("Preview", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def frames2ascii(color, res):
    filenum = 0
    pid = []
    numfiles = len(
        [name for name in os.listdir("temp/frames_in/") if os.path.isfile(os.path.join("temp/frames_in/", name))])
    finishedfiles = 0
    workingfiles = 0
    charlist = sortfonts(color)
    cpucount = multiprocessing.cpu_count()

    charw = math.floor(charlist[0] // res)
    charh = math.floor(charlist[1] // res)

    while workingfiles != numfiles and finishedfiles < numfiles:

        while len(pid) < cpucount:
            path = f'./temp/frames_in/{filenum}.jpg'
            p = Process(target=procstart, args=(path, filenum, charlist, [charw, charh]))
            pid.append(p)
            workingfiles += 1
            p.start()
            filenum += 1

        deadprocess = []
        for i in range(len(pid)):
            if not pid[i].is_alive():
                finishedfiles += 1
                print(f'{100 * finishedfiles / numfiles:5.2f}' + "% fertig")
                pid[i].join()
                deadprocess.append(i)
        deadprocess.reverse()
        for i in deadprocess:
            pid.pop(i)

    print("100%")
    print("Frames in Ascii umgewandelt.")


def procstart(path, framenum, charlist, charsize):
    img = cv2.imread(path)
    try:
        img = cv2.resize(img, [1920, 1080])
    except:
        print(framenum)
    img2ascii(img, framenum, charlist, charsize)
