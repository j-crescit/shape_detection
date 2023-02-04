"""
Test video file before applying to webcam file(main.py)
"""

import cv2
import numpy as np

cap = cv2.VideoCapture('video/rec_1.mp4')

def empty(a):
    pass

cv2.namedWindow('Parameters')
cv2.resizeWindow('Parameters', 640, 240)
cv2.createTrackbar('Threshold_1', 'Parameters', 25, 255, empty)
cv2.createTrackbar('Threshold_2', 'Parameters', 240, 255, empty)
cv2.createTrackbar("Area", "Parameters", 1000, 100000, empty)

y_list=[]

fourcc = cv2.VideoWriter_fourcc(*'DIVX')

width = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

out = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))

def getContours(img, imgContours):

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for i in contours:
        area = cv2.contourArea(i)
        area_min = cv2.getTrackbarPos("Area", "Parameters")

        M = cv2.moments(i, False)

        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
        else:
            cX = 0
            cY = 0

        y_list.append(abs(360 - cY))

        amplitude = round(abs(2 * (360 - cY)/94.2), 3)
        max_amplitude = round(2 * (max(y_list))/94.2, 3)

        print(max_amplitude)

        cv2.circle(img_contour, (cX, cY), 4, (255, 0, 0), -1)
        cv2.drawContours(img_contour, [i], 0, (0, 255, 255), 2)

        if area > area_min:
            cv2.drawContours(img_contour, i, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            # print(len(approx))
            # print(str(int(cY)))
            x, y, w, h = cv2.boundingRect(approx)

            cv2.rectangle(img_contour, (x, y), (x+w, y+h), (0, 255, 0), 5)

            cv2.putText(img_contour, 'Points : ' + str(len(approx)), (20, 40), cv2.FONT_HERSHEY_COMPLEX, 0.75, (212, 175, 55), 1)
            # cv2.putText(img_contour, 'Mass Center  : ' + str(int(880 - cX)) + ' ,' + str(int(360 - cY)), (20, 75), cv2.FONT_HERSHEY_COMPLEX, 0.75, (212, 175, 55), 1)
            # cv2.putText(img_contour, 'Area : ' + str(int(area)), (20, 75), cv2.FONT_HERSHEY_COMPLEX, 0.5, (212, 175, 55), 1)
            cv2.putText(img_contour, 'Amplitude : ' + str(amplitude) + 'mm', (20, 75), cv2.FONT_HERSHEY_COMPLEX, 0.75, (212, 175, 55), 1)
            cv2.putText(img_contour, 'Max Amplitude : ' + str(max_amplitude) + 'mm', (20, 110), cv2.FONT_HERSHEY_COMPLEX, 0.75, (212, 175, 55), 1)


while True:
    success, img = cap.read()
    img_contour = img.copy()

    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold_1 = cv2.getTrackbarPos('Threshold_1', 'Parameters')
    threshold_2 = cv2.getTrackbarPos('Threshold_2', 'Parameters')

    img_Canny = cv2.Canny(imgGray, threshold_1, threshold_2)
    kernel = np.ones((5, 5))
    img_dil = cv2.dilate(img_Canny, kernel, iterations=1)

    getContours(img_dil, img_contour)

    out.write(img_contour)

    cv2.imshow('Result', img_contour)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

