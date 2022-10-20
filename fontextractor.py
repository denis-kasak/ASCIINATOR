import csv
import os
import shutil

import cv2


def main():
    maxx = 0
    maxy = 0

    img = cv2.imread("./res/fontmap.png", cv2.IMREAD_UNCHANGED)

    if os.path.exists("./res/chars/"):
        shutil.rmtree("./res/chars/")
    os.mkdir("./res/chars/")

    with open('./res/coords.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                maxx = int(row[5])
                maxy = int(row[6])
                line_count += 1
            elif line_count == 1:
                line_count += 1
                pass
            else:
                x1 = int(row[1])
                y1 = int(row[2])
                x2 = int(row[3]) + 1
                y2 = int(row[4]) + 1
                w = x2 - x1
                h = y2 - y1

                if w < maxx:
                    diff = maxx - w
                    abstand = diff // 2
                    if diff % 2 == 0:
                        x1 = x1 - abstand
                        x2 = x2 + abstand
                    else:
                        x1 = x1 - abstand
                        x2 = x2 + abstand + 1
                if h < maxy:
                    diff = maxy - h
                    abstand = diff // 2
                    if diff % 2 == 0:
                        y1 = y1 - abstand
                        y2 = y2 + abstand
                    else:
                        y1 = y1 - abstand
                        y2 = y2 + abstand + 1

                crop_img = img[y1:y2, x1:x2]

                cv2.imwrite("./res/chars/" + str(line_count - 2) + ".png", crop_img)
                line_count += 1


def sortfonts():
    i = 0
    charlist = []
    while os.path.isfile("./res/chars/" + str(i) + ".png"):
        path = "./res/chars/" + str(i) + ".png"
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        h = img.shape[0]
        w = img.shape[1]

        avg = 0

        for x in range(0, w):
            for y in range(0, h):
                px = img[y, x]
                avg += px[3]
        avg = avg / ((w - 1) * (h - 1))
        charlist.append([avg, os.path.abspath(path)])
        i = i + 1
    charlist = sorted(charlist)

    minv = 1000
    maxv = 0
    for i in range(len(charlist)):
        if charlist[i][0] < minv:
            minv = charlist[i][0]
        elif charlist[i][0] > maxv:
            maxv = charlist[i][0]
    for i in range(len(charlist)):
        charlist[i][0] = (charlist[i][0] - minv) / maxv

    with open('./res/coords.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            maxx = int(row[5])
            maxy = int(row[6])
            break;
        return [maxx, maxy, charlist]


if __name__ == '__main__':
    main()
    #print(sortfonts())
