import cv2
import numpy as np
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import csv
import pytesseract

# Opening the video file
cap = cv2.VideoCapture('E:\Work\pythonProjects\engage_measure\example1.mp4')

# cap.set(cv2.CAP_PROP_POS_MSEC, 670500)  # to start the video at a specific time in milliseconds
current_time_ms = 675000    # 0

# person joining status
hasib_joined = False
soha_joined = False
both_joined = False

#   creating csv file for screen sharing record-keeping
f = open('scrn_shr_rcrd.csv', 'w', newline='')
writer = csv.writer(f)
header = ['Time in seconds', '#Contours', 'Screen Sharing', 'Hasib joined', 'Soha joined', 'Date', 'Time']
writer.writerow(header)

while True:
    cap.set(cv2.CAP_PROP_POS_MSEC, current_time_ms)  # to start the video at a specific time in milliseconds
    ret, im = cap.read()    # reading the video
    if ret is False:
        break

    im = cv2.resize(im, (1080, 720), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

    #   converting the video to a processable format
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 100, 230, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cnt = contours[-1]
    cv2.drawContours(im, contours, -1, (0, 255, 0), 1)

    contcnt = len(contours)  # counting the number of contours
    cv2.putText(im, "#Contours: " + str(contcnt), (70, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    current_time = int(current_time_ms / 1000)   # calculating the current time in seconds
    cv2.putText(im, "Video time: " + str(current_time) + "s", (70, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)

    #   displaying information of screen sharing on the video
    if contcnt>100:
        cv2.putText(im, ":Screen is being shared:", (650, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 150), 2)
    else:
        cv2.putText(im, ":Waiting time:", (750, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 50, 200), 2)

    # print("got here")
    #   joining-time detection
    # text = pytesseract.image_to_string(thresh)
    # print(text)
    if not contcnt>100:
        text = pytesseract.image_to_string(thresh)  # detecting text from image
        name, _, dt_n_tm = text.splitlines()
        date, time = dt_n_tm.split()
        # print(name)
        # print(date)
        # print(time)
    else:
        date, time = '', ''

    if not both_joined:
        if (not hasib_joined) and (name == 'hasib'):
            hasib_joined = True
        elif (not soha_joined) and (name == 'sohas' or name == 'soha$'):
            soha_joined = True

        if hasib_joined & soha_joined:
            both_joined = True

    #   writing screen-share data into the csv file (~this has to be modified for inputting data per second~)
    writer.writerow([current_time, contcnt, contcnt>100, hasib_joined, soha_joined, date, time])

    #   displaying the video
    cv2.imshow("Contour video", im)

    # incrementing the loop iterator by one second (1000ms)
    # (this will read the video-frames only per second. Not sure if this is quite alright to do)
    current_time_ms += 1000

    key = cv2.waitKey(1)
    if key == 27:   # 27 is the 'escape' key
        break

#   closing the screen recorder csv file
f.close()

#   plotting the data
# plt.rcParams["figure.figsize"] = [7.50, 3.50]
# plt.rcParams["figure.autolayout"] = True
#
# df = pd.read_csv('scrn_shr_rcrd.csv')
#
# df.set_index('Time').plot()
#
# plt.show()
