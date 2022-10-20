import glob
import multiprocessing
import os
import shutil
from multiprocessing import Process

import cv2

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


def img2ascii(img, indeximg, charlist):
    maxx = charlist[0]
    maxy = charlist[1]
    charlist = charlist[2]

    maxx = maxx // 3
    maxy = maxy // 3

    h = img.shape[0]
    w = img.shape[1]

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    matrix = []

    for y in range(h):
        matrix.append([])
        for x in range(w):
            matrix[y].append([])
            matrix[y][x] = img[y][x] / 256

    piclist = []

    for y in range(0, h, maxy):
        piclist.append([])
        for x in range(0, w, maxx):
            piclist[y // maxy].append([])
            avg = 0
            for i in range(maxx):
                for j in range(maxy):
                    try:
                        avg += matrix[y + j][x + i]
                    except IndexError:
                        pass
            avg = avg / (maxx * maxy)
            i_closest = getclosest(charlist, avg)
            piclist[y // maxy][x // maxx] = charlist[i_closest][1]

    for y in range(len(piclist)):
        piclist[y] = cv2.hconcat(piclist[y])
    piclist = cv2.vconcat(piclist)

    piclist = cv2.resize(piclist, [1920,1080])

    cv2.imwrite("./frames_out/" + str(indeximg) + ".png", piclist)


def prepcharlist(charlist):
    for i in range(len(charlist[2])):
        charlist[2][i][1] = cv2.imread(charlist[2][i][1])
    return charlist


def frames2ascii():
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
            p = Process(target=procstart, args=(path, i, charlist))
            pid.append(p)
            p.start()
            i += 1
    print("100.00% fertig")


def procstart(path, i, charlist):
    img = cv2.imread(path)
    img2ascii(img, i, charlist)


def combinevideo():
    img_array = []
    # for filename in glob.glob('./frames_out/*.jpg'):
    i = 0
    while os.path.isfile("./frames_out/" + str(i) + ".png"):
        path = "./frames_out/" + str(i) + ".png"
        img = cv2.imread(path)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
        i += 1

    if os.path.isfile('output.mp4'):
        shutil.rmtree("output.mp4")

    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'h264'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

combinevideo()
