import cv2


def splitVideo(path):
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
