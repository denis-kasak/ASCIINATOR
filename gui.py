import os.path
import tkinter as tk
from tkinter.filedialog import askopenfilename
import cv2

from imgprocessor import frames2ascii, combinevideo
from splitvideo import splitVideo


def processVideo():
    videoPath = askopenfilename(filetypes=[("Videos", "*")])
    splitVideo(videoPath)
    frames2ascii()
    combinevideo()


def buildGui():
    window = tk.Tk()

    window.geometry("100x100")

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
