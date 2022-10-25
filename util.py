import os
import shutil
from bisect import bisect_left
import cv2
import time


def _take_closesthelp(lst, k):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - k))]

def take_closesthelp(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before


def initdir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)


def getclosest(charlist, target):
    nlist = []
    for i in range(len(charlist)):
        nlist.append(charlist[i][0])
    target = take_closesthelp(nlist, target)
    for i in range(len(charlist)):
        if charlist[i][0] == target:
            return i


def combinevideo(srcdir, target, codec, fps):
    img_array = []
    i = 0

    while os.path.isfile(srcdir + str(i) + ".jpg"):
        path = srcdir + str(i) + ".jpg"
        img = cv2.imread(path)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
        i += 1

    if os.path.isfile(target):
        os.remove(target)

    out = cv2.VideoWriter(target, cv2.VideoWriter_fourcc(*codec), fps, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


def splitVideo(videopath):

    capture = cv2.VideoCapture(videopath)
    frameNr = 0


    while True:
        success, frame = capture.read()
        if success:
            cv2.imwrite(f'./temp/frames_in/{frameNr}.jpg', frame)
        else:
            break
        frameNr += 1

    capture.release()
    print("Video in Frames einteilen beendet.")

def inittemp():
    initdir("./temp/")
    initdir("./temp/frames_in/")
    initdir("./temp/frames_out/")
    initdir("./temp/chars/")
