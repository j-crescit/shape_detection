"""
Test image file before applying to webcam file(main.py)
"""

import numpy as np
import cv2

image = cv2.imread('image/shape.png')

image_rst = cv2.resize(image, dsize = (0, 0), fx = 0.5, fy = 0.5, interpolation=cv2.INTER_LINEAR)

def getContours(img, imgContours):

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for i in contours:
        area = cv2.contourArea(i)
        area_min = 5000

        M = cv2.moments(i, False)

        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
        else:
            cX = 0
            cY = 0

        cv2.circle(img_contour, (cX, cY), 4, (255, 0, 0), -1)
        cv2.drawContours(img_contour, [i], 0, (0, 255, 255), 2)

        if area > area_min:
            cv2.drawContours(img_contour, i, -1, (255, 215, 0), 5)
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)

            cv2.rectangle(img_contour, (x, y), (x+w, y+h), (100, 150, 150), 2)

            cv2.putText(img_contour, 'Points : ' + str(len(approx)), (x + w + 10, y + 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (100, 150, 150), 1)
            cv2.putText(img_contour, 'Area : ' + str(int(area)), (x + w + 10, y + 35), cv2.FONT_HERSHEY_COMPLEX, 0.5, (100, 150, 150), 1)
            cv2.putText(img_contour, 'Mass Center  : ' + '(' + str(int(cX)) + ' , ' + str(int(cY))  + ')', (x + w + 10, y + 60), cv2.FONT_HERSHEY_COMPLEX, 0.5, (100, 150, 150), 1)

img_contour = image.copy()

img_blur = cv2.GaussianBlur(image, (7, 7), 1)
img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

img_canny = cv2.Canny(img_gray, 25, 240)
kernel = np.ones((5, 5))
img_dil = cv2.dilate(img_canny, kernel, iterations = 1)

getContours(img_dil, img_contour)

cv2.imshow('shape detection', img_contour)
cv2.waitKey(0)
cv2.destroyAllWindows()