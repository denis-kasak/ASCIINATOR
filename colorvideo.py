import multiprocessing
import os
import shutil
from multiprocessing import Process

import cv2

from splitvideo import splitVideo


def colorvideo(bgr):
    splitVideo("output.mp4")
    frames2ascii(bgr)


def _colorvideo(img, i, bgr):
    for y in range(len(img)):
        for x in range(len(img[y])):
            faktor = img[y][x][0] / 256
            img[y][x][0] = bgr[0] * faktor
            img[y][x][1] = bgr[1] * faktor
            img[y][x][2] = bgr[2] * faktor
    cv2.imwrite("./frames_out/" + str(i) + ".jpg", img)


def frames2ascii(bgr):
    shutil.rmtree("./frames_out/")
    os.mkdir("./frames_out/")
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
            p = Process(target=procstart, args=(path, i, bgr))
            pid.append(p)
            p.start()
            i += 1
    for j in pid:
        j.join()
    print("100.00% fertig")


def procstart(path, i, bgr):
    img = cv2.imread(path)
    _colorvideo(img, i, bgr)


def combinevideo():
    img_array = []
    i = 0

    while os.path.isfile("./frames_out/" + str(i) + ".jpg"):
        path = "./frames_out/" + str(i) + ".jpg"
        img = cv2.imread(path)
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


