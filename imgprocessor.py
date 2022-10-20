import multiprocessing
import os
import time
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


def img2ascii(img, indeximg):
    charlist = sortfonts()

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

    start = time.time()
    for i in range(len(piclist)):
        for j in range(len(piclist[i])):
            piclist[i][j] = cv2.imread(piclist[i][j], cv2.IMREAD_UNCHANGED)
    end = time.time()
    print("for2: " + str(end - start))
    start = time.time()
    for y in range(len(piclist)):
        piclist[y] = cv2.hconcat(piclist[y])
    end = time.time()
    print("for3: " + str(end - start))
    piclist = cv2.vconcat(piclist)

    cv2.imwrite("./frames_out/" + str(indeximg) + ".png", piclist)


def processalive(p):
    if p.poll() is None:
        return True
    else:
        return False


def frames2ascii():
    i = 0
    pid = []
    ready = True
    numfiles = len([name for name in os.listdir("./frames_in/") if os.path.isfile(os.path.join("./frames_in/", name))])
    finishedfiles = 0

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
            p = Process(target=procstart, args=(path, i))
            pid.append(p)
            p.start()
            i += 1
    print("100.00% fertig")


def procstart(path, i):
    img = cv2.imread(path)
    img2ascii(img, i)
