import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
import imgprocessor
import util

path = ""
font_bgr = []
bg_bgr = []


def processVideo():
    util.splitVideo(path)
    imgprocessor.frames2ascii([font_bgr, bg_bgr])
    util.combinevideo("./temp/frames_out/", "output.mp4", "mp4v", 30)


def setpath():
    global path
    path = askopenfilename(filetypes=[("Videos", "*")])


def setfontcolor():
    color = askcolor(color=None)[0]
    global font_bgr
    font_bgr.append(color[2])
    font_bgr.append(color[1])
    font_bgr.append(color[0])


def setbgcolor():
    color = askcolor(color=None)[0]
    global bg_bgr
    bg_bgr.append(color[2])
    bg_bgr.append(color[1])
    bg_bgr.append(color[0])


def buildGui():
    window = tk.Tk()

    window.geometry("200x200")

    frame_a = tk.Frame()

    label_a = tk.Label(master=frame_a, text="Video in Charakter umwandeln:")
    label_a.pack()

    btnVideo = tk.Button(frame_a, text="Video auswählen", command=(lambda: setpath()))
    btnVideo.pack()

    btnFontColor = tk.Button(frame_a, text="Schriftfarbe auswählen", command=(lambda: setfontcolor()))
    btnFontColor.pack()

    btnBgColor = tk.Button(frame_a, text="Hintergrundfarbe auswählen", command=(lambda: setbgcolor()))
    btnBgColor.pack()

    btnStart = tk.Button(frame_a, text="start", command=(lambda: processVideo()))
    btnStart.pack()

    frame_a.pack()

    window.mainloop()


def main():
    buildGui()


if __name__ == '__main__':
    main()
