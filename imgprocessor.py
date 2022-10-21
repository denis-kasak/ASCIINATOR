import glob
import math
import multiprocessing
import os
import shutil
from multiprocessing import Process

import splitvideo
from splitvideo import splitVideo

import cv2
import numpy
from fontextractor import sortfonts


def take_closesthelp(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


def getclosest(charlist, target):
    nlist = []
    for i in range(len(charlist)):
        nlist.append(charlist[i][0])
    target = take_closesthelp(nlist, target)
    for i in range(len(charlist)):
        if (charlist[i][0] == target):
            return i


def img2ascii(img, indeximg, charlist, bgr):
    maxx = charlist[0]
    maxy = charlist[1]
    charlist = charlist[2]

    maxx = maxx // 4
    maxy = maxy // 4

    h = img.shape[0]
    w = img.shape[1]

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    piclist = []

    start = time.time()
    for y in range(0, h, maxy):
        piclist.append([])
        for x in range(0, w, maxx):
            piclist[y // maxy].append([])
            avg = 0
            for i in range(maxx):
                for j in range(maxy):
                    try:
                        avg += img[y + j][x + i] / 256
                    except IndexError:
                        pass
            avg = avg / (maxx * maxy)
            i_closest = getclosest(charlist, avg)
            piclist[y // maxy][x // maxx] = charlist[i_closest][1]
    end = time.time()
    print("for1: " + str(end - start))

    for y in range(len(piclist)):
        piclist[y] = cv2.hconcat(piclist[y])
    end = time.time()
    print("for3: " + str(end - start))
    piclist = cv2.vconcat(piclist)

    piclist = cv2.resize(piclist, [1920, 1080])

    cv2.imwrite("./frames_out/" + str(indeximg) + ".png", piclist)


def prepcharlist(charlist):
    for i in range(len(charlist[2])):
        charlist[2][i][1] = cv2.imread(charlist[2][i][1], cv2.IMREAD_UNCHANGED)
    return charlist


def frames2ascii(bgr):
    if os.path.exists("./frames_out/"):
        shutil.rmtree("./frames_out/")
    os.mkdir("./frames_out/")
    i = 0
    pid = []
    ready = True
    numfiles = len([name for name in os.listdir("./frames_in/") if os.path.isfile(os.path.join("./frames_in/", name))])
    finishedfiles = 0
    charlist = sortfonts()
    charlist = prepcharlist(charlist)

    while os.path.isfile("./frames_in/frame_" + str(i) + ".jpg"):

        if len(pid) == multiprocessing.cpu_count():
            for j in range(len(pid)):
                if not pid[j].is_alive():
                    finishedfiles += 1
                    print(f'{100 * finishedfiles / numfiles:5.2f}' + "% fertig")
                    pid[j].join()
                    pid.pop(j)
                    ready = True
                    break
                ready = False

        if ready:
            path = "./frames_in/frame_" + str(i) + ".jpg"
            p = Process(target=procstart, args=(path, i, charlist, bgr))
            pid.append(p)
            p.start()
            i += 1
    for j in pid:
        j.join()
    print("100.00% fertig")


def procstart(path, i, charlist, bgr):
    img = cv2.imread(path)
    img2ascii(img, i, charlist, bgr)


def combinevideo():
    img_array = []
    i = 0

    while os.path.isfile("./frames_out/" + str(i) + ".png"):
        path = "./frames_out/" + str(i) + ".png"
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
        i += 1

    if os.path.isfile('output.mp4'):
        os.remove("output.mp4")

    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'h264'), 30, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()



