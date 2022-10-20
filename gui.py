import os.path
import time
import tkinter as tk
from tkinter.filedialog import askopenfilename
import cv2

from imgprocessor import frames2ascii
from splitvideo import splitVideo


def combineVideo():
    image_folder = './frames_in/'
    video_name = 'video.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


def processVideo():
    start = time.time()
    videoPath = askopenfilename(filetypes=[("Videos", "*")])
    splitVideo(videoPath)
    frames2ascii()
    end = time.time()
    print("Umwandlung dauerte "+str(end-start)+" Sekunden")


def buildGui():
    window = tk.Tk()

    window.geometry("500x500")

    frame_a = tk.Frame()
    label_a = tk.Label(master=frame_a, text="I'm in Frame A")
    label_a.pack()

    btnFile = tk.Button(frame_a, text="Video auswählen", command=(lambda: processVideo()))
    btnFile.pack()

    frame_a.pack()

    window.mainloop()


def main():
    buildGui()


if __name__ == '__main__':
    main()
