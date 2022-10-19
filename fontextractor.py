import csv

import cv2

maxx = 0
maxy = 0

img = cv2.imread("./res/fontmap.png", cv2.IMREAD_UNCHANGED)

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
                abstand = diff//2
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

            cv2.imwrite("./res/chars/char" + str(line_count) + ".png", crop_img)
            line_count += 1
