import tkinter as tk
from tkinter.filedialog import askopenfilename

videoPath = ""


def getVideo():
    videoPath = askopenfilename(filetypes=[("Videos", "*.mp4")])
    pass


def buildGui():
    window = tk.Tk()

    window.geometry("500x500")

    frame_a = tk.Frame()
    label_a = tk.Label(master=frame_a, text="I'm in Frame A")
    label_a.pack()

    btnFile = tk.Button(frame_a, text="Video auswählen", command=getVideo)
    btnFile.pack()

    frame_a.pack()

    window.mainloop()


def splitVideo():
    pass


def main():
    buildGui()
    while videoPath != "":
        pass


if __name__ == '__main__':
    main()
