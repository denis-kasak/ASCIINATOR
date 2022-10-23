import math
import multiprocessing
import os
import shutil
from multiprocessing import Process
import cv2
from fontextractor import sortfonts
from util import getclosest


def img2ascii(img, indeximg, charlist, color):
    charw = charlist[0]
    charh = charlist[1]
    charlist = charlist[2]

    charw = math.floor(charw // 0.5)
    charh = math.floor(charh // 0.5)

    h = img.shape[0]
    w = img.shape[1]

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    nimg = []
    for y in range(h):
        nimg.append([])
        for x in range(w):
            nimg[y].append([])
            nimg[y][x] = int(img[y][x]) / 256
    img = nimg

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


def frames2ascii(color):
    if os.path.exists("temp/frames_out/"):
        shutil.rmtree("temp/frames_out/")
    os.mkdir("temp/frames_out/")
    filenum = 0
    pid = []
    numfiles = len(
        [name for name in os.listdir("temp/frames_in/") if os.path.isfile(os.path.join("temp/frames_in/", name))])
    finishedfiles = 0
    workingfiles = 0
    charlist = sortfonts()
    cpucount = multiprocessing.cpu_count()

    while workingfiles != numfiles and finishedfiles < numfiles:

        while len(pid) < cpucount:
            path = f'./temp/frames_in/{filenum}.jpg'
            p = Process(target=procstart, args=(path, filenum, charlist, color))
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


def procstart(path, framenum, charlist, bgr):
    img = cv2.imread(path)
    img = cv2.resize(img, [1920, 1080])
    img2ascii(img, framenum, charlist, bgr)
