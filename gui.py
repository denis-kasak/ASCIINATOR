import os.path
import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
import cv2

from imgprocessor import frames2ascii, combinevideo
from splitvideo import splitVideo

path = ""
bgr = []


def processVideo():
    splitVideo(path)
    frames2ascii(bgr)
    combinevideo()


def setpath():
    global path
    path = askopenfilename(filetypes=[("Videos", "*")])


def setcolor():
    input = askcolor(color=None)[0]
    global bgr
    bgr.append(input[2])
    bgr.append(input[1])
    bgr.append(input[0])


def buildGui():
    window = tk.Tk()

    window.geometry("200x200")

    frame_a = tk.Frame()

    label_a = tk.Label(master=frame_a, text="Video in Charakter umwandeln:")
    label_a.pack()

    btnVideo = tk.Button(frame_a, text="Video auswählen", command=(lambda: setpath()))
    btnVideo.pack()

    btnColor = tk.Button(frame_a, text="Farbe auswählen", command=(lambda: setcolor()))
    btnColor.pack()

    btnStart = tk.Button(frame_a, text="start", command=(lambda: processVideo()))
    btnStart.pack()

    frame_a.pack()

    window.mainloop()


def main():
    buildGui()


if __name__ == '__main__':
    main()
