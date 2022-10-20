import os
import shutil

import cv2


def splitVideo(path):

    if os.path.exists("./frames_in/"):
        shutil.rmtree("./frames_in/")
    os.mkdir("./frames_in/")

    capture = cv2.VideoCapture(path)

    frameNr = 0

    while True:

        success, frame = capture.read()

        if success:
            cv2.imwrite(f'./frames_in/frame_{frameNr}.jpg', frame)

        else:
            break

        frameNr = frameNr + 1

    capture.release()
