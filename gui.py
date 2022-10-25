import tkinter as tk
from tkinter import HORIZONTAL
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
import fontextractor
import imgprocessor
import util
import cProfile

path = ""
font_bgr = [255, 255, 255]
bg_bgr = [0, 0, 0]
items = ""
scale = ""


def processVideo():
    util.inittemp()
    res = scale.get() / 10
    fontextractor.setskin(items.get())
    util.splitVideo(path)
    imgprocessor.frames2ascii([font_bgr, bg_bgr], res)
    util.combinevideo("./temp/frames_out/", "output.mp4", "h264", 30)
    print("Video ist fertig.")


def preview():
    util.inittemp()
    res = scale.get() / 10
    fontextractor.setskin(items.get())
    img = util.firstframe(path)
    imgprocessor.singleframe([font_bgr, bg_bgr], res, img)


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

    master = tk.Frame()

    label_a = tk.Label(master=master, text="Video in Charakter umwandeln:")
    label_a.pack()

    btnVideo = tk.Button(master, text="Video auswählen", command=(lambda: setpath()))
    btnVideo.pack()

    btnFontColor = tk.Button(master, text="Schriftfarbe auswählen", command=(lambda: setfontcolor()))
    btnFontColor.pack()

    btnBgColor = tk.Button(master, text="Hintergrundfarbe auswählen", command=(lambda: setbgcolor()))
    btnBgColor.pack()

    labelskin = tk.Label(master, text="Characterset wählen:")
    labelskin.pack()

    skinlist = fontextractor.getskins()
    global items
    items = tk.StringVar(master)
    items.set(skinlist[0])
    dropdown = tk.OptionMenu(master, items, *skinlist)
    dropdown.pack()

    labelres = tk.Label(master, text="Auflösung wählen:")
    labelres.pack()

    global scale
    scale = tk.Scale(master, from_=10, to=40, orient=HORIZONTAL)
    scale.set(25)
    scale.pack()

    btnpreview = tk.Button(master, text="Vorschau", command=(lambda: preview()))
    btnpreview.pack()

    btnStart = tk.Button(master, text="start", command=(lambda: processVideo()))
    btnStart.pack()

    master.pack()

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
