import cv2
import numpy as np
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import csv

# im = cv2.imread('waiting time hasib.png')

cap = cv2.VideoCapture('E:\Work\Academics\Thesis Saad\example1.mp4')
cap.set(cv2.CAP_PROP_POS_MSEC, 670500)  # to start the video at a specific time in milliseconds

#   creating csv file for screen sharing record-keeping
f = open('scrn_shr_rcrd.csv', 'w', newline='')
writer = csv.writer(f)
header = ['Time', 'Screen Sharing']
writer.writerow(header)

while True:
    ret, im = cap.read()
    if ret is False:
        break

    im = cv2.resize(im, (1080, 720), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 100, 230, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cnt = contours[-1]
    cv2.drawContours(im, contours, -1, (0, 255, 0), 1)

    contcnt = len(contours)  # counting the number of contours
    cv2.putText(im, "#Contours: " + str(contcnt), (70, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    current_time = int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
    cv2.putText(im, "Video time: " + str(current_time) + "s", (70, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
    # print("Time in seconds: ", current_time)

    if contcnt>100:
        cv2.putText(im, ":Screen is being shared:", (650, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 150), 2)
    else:
        cv2.putText(im, ":Waiting time:", (750, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 50, 200), 2)

    #   writing data into the csv file
    writer.writerow([current_time, contcnt>100])

    cv2.imshow("Contour video", im)
    # print("Number of contours: ", contcnt)

    key = cv2.waitKey(10)
    if key == 27:   # 27 is the 'escape' key
        break

#   closing the screen recorder csv file
f.close()

#   plotting the data
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

df = pd.read_csv('scrn_shr_rcrd.csv')

df.set_index('Time').plot()

plt.show()
