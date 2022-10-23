import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename

import fontextractor
import imgprocessor
import util

path = ""
font_bgr = [255, 255, 255]
bg_bgr = [0, 0, 0]
items = ""


def processVideo():
    fontextractor.setskin(items.get())
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
        font_bgr[2] = color[2]
        font_bgr[1] = color[1]
        font_bgr[0] = color[0]


def setbgcolor():
    color = askcolor(color="black")[0]
    global bg_bgr
    if color is not None:
        bg_bgr[2] = color[2]
        bg_bgr[1] = color[1]
        bg_bgr[0] = color[0]


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
    global items
    items = tk.StringVar(frame_a)
    items.set(skinlist[0])
    dropdown = tk.OptionMenu(frame_a, items, *skinlist)
    dropdown.pack()

    btnStart = tk.Button(frame_a, text="start", command=(lambda: processVideo()))
    btnStart.pack()

    frame_a.pack()

    centerwin(window)

    window.mainloop()


def centerwin(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


if __name__ == '__main__':
    buildGui()
