import os.path
import subprocess
import tkinter as tk
from tkinter.filedialog import askopenfilename
import cv2

from splitvideo import splitVideo
import shutil


def getVideo():
    videoPath = askopenfilename(filetypes=[("Videos", "*")])
    if os.path.exists("./frames_in/"):
        shutil.rmtree("./frames_in/")
    os.mkdir("./frames_in/")
    splitVideo(videoPath)
    pass


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
    getVideo()

    # c++ Programm wird gestartet
    p = subprocess.Popen(['a.exe', ''])
    while p.poll() is None:
        pass
    # c++ Programm ist fertig
    combineVideo()


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
