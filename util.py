import os
import shutil
import cv2


def initdir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


def combinevideo(srcdir, target, codec, fps):
    img_array = []
    i = 1

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


def inittemp():
    initdir("./temp/")
    initdir("./temp/frames_in/")
    initdir("./temp/frames_out/")
    initdir("./temp/chars/")


def firstframe(videopath):
    capture = cv2.VideoCapture(videopath)

    success, frame = capture.read()
    capture.release()

    return frame
