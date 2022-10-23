import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename

import fontextractor
import imgprocessor
import util

path = ""
font_bgr = []
bg_bgr = []


def processVideo():
    util.splitVideo(path)
    imgprocessor.frames2ascii([font_bgr, bg_bgr])
    util.combinevideo("./temp/frames_out/", "output.mp4", "mp4v", 30)
    print("Video ist fertig.")


def setpath():
    global path
    path = askopenfilename(filetypes=[("Videos", "*")])


def setfontcolor():
    color = askcolor(color="green")[0]
    global font_bgr
    if color is not None:
        font_bgr.append(color[2])
        font_bgr.append(color[1])
        font_bgr.append(color[0])
    else:
        font_bgr.append(255)
        font_bgr.append(255)
        font_bgr.append(255)


def setbgcolor():
    color = askcolor(color="black")[0]
    global bg_bgr
    if color is not None:
        bg_bgr.append(color[2])
        bg_bgr.append(color[1])
        bg_bgr.append(color[0])
    else:
        bg_bgr.append(0)
        bg_bgr.append(0)
        bg_bgr.append(0)


def buildGui():
    window = tk.Tk()

    window.geometry("300x300")

    frame_a = tk.Frame()

    label_a = tk.Label(master=frame_a, text="Video in Charakter umwandeln:")
    label_a.pack()

    btnVideo = tk.Button(frame_a, text="Video auswählen", command=(lambda: setpath()))
    btnVideo.pack()

    btnFontColor = tk.Button(frame_a, text="Schriftfarbe auswählen", command=(lambda: setfontcolor()))
    btnFontColor.pack()

    btnBgColor = tk.Button(frame_a, text="Hintergrundfarbe auswählen", command=(lambda: setbgcolor()))
    btnBgColor.pack()

    labelskin = tk.Label(frame_a, text="Characterset wählen:")
    labelskin.pack()

    skinlist = fontextractor.getskins()
    items = tk.StringVar(frame_a)
    items.set(skinlist[0])
    dropdown = tk.OptionMenu(frame_a, items, *skinlist, command=fontextractor.setskin)
    dropdown.pack()

    btnStart = tk.Button(frame_a, text="start", command=(lambda: processVideo()))
    btnStart.pack()

    frame_a.pack()

    window.mainloop()


if __name__ == '__main__':
    buildGui()
