import math
import multiprocessing
import os
from multiprocessing import Process

import cv2
import time

import util
from fontextractor import sortfonts
from util import getclosest


def img2ascii(img, indeximg, charlist, res):
    charw = math.floor(charlist[0] // res)
    charh = math.floor(charlist[1] // res)

    charlist = charlist[2]

    h = img.shape[0]
    w = img.shape[1]

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if h != 1080 or w != 1920:
        img = cv2.resize(img, [1920, 1080])

    piclist = []

    for y in range(0, h, charh):
        piclist.append([])
        for x in range(0, w, charw):
            piclist[y // charh].append([])
            avg = 0
            for i in range(charw):
                for j in range(charh):
                    try:
                        avg += img[y + j][x + i]
                    except IndexError:
                        pass

            avg = avg / (charw * charh)
            i_closest = getclosest(charlist, avg)
            piclist[y // charh][x // charw] = charlist[i_closest][1]

    for y in range(len(piclist)):
        piclist[y] = cv2.hconcat(piclist[y])
    piclist = cv2.vconcat(piclist)

    piclist = cv2.resize(piclist, [1920, 1080])

    cv2.imwrite(f'./temp/frames_out/{indeximg}.jpg', piclist)


def singleframe(color, res, path):
    capture = cv2.VideoCapture(path)
    img = capture.read()[1]
    capture.release()
    charlist = sortfonts(color)
    img2ascii(img, 0, charlist, res)

    img = cv2.imread("./temp/frames_out/0.jpg")

    cv2.imshow("Preview", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def frames2ascii(color, res):
    util.initdir("temp/frames_out/")
    filenum = 0
    pid = []
    numfiles = len(
        [name for name in os.listdir("temp/frames_in/") if os.path.isfile(os.path.join("temp/frames_in/", name))])
    finishedfiles = 0
    workingfiles = 0
    charlist = sortfonts(color)
    cpucount = multiprocessing.cpu_count()

    while workingfiles != numfiles and finishedfiles < numfiles:

        while len(pid) < cpucount:
            path = f'./temp/frames_in/{filenum}.jpg'
            p = Process(target=procstart, args=(path, filenum, charlist, res))
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


def procstart(path, framenum, charlist, res):
    img = cv2.imread(path)
    img = cv2.resize(img, [1920, 1080])
    img2ascii(img, framenum, charlist, res)
