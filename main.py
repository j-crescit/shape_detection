import numpy as np
import cv2

cap = cv2.VideoCapture(1)

cap.set(3, 400)
cap.set(4, 300)

def empty(a):
    pass

cv2.namedWindow('Parameters')
cv2.resizeWindow('Parameters', 640, 240)
cv2.createTrackbar('Threshold_1', 'Parameters', 25, 255, empty)
cv2.createTrackbar('Threshold_2', 'Parameters', 240, 255, empty)
cv2.createTrackbar("Area", "Parameters", 5000, 30000, empty)

def stackImage(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])

    rowsAvailable = isinstance(imgArray[0], list)

    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]

    if rowsAvailable:
        for x in range(0, rows):

            for y in range(0, cols):

                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)

                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)

                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)

        imageBlank = np.zeros((height, width, 3), np.uint8)

        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows

        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])

        ver = np.vstack(hor)

    else:
        for x in range(0, rows):

            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)

            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)

            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)

        hor = np.hstack(imgArray)
        ver = hor
    return ver

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

        cv2.circle(img_contour, (cX, cY), 4, (255, 0, 0), -1)
        cv2.drawContours(img_contour, [i], 0, (0, 255, 255), 2)

        if area > area_min:
            cv2.drawContours(img_contour, i, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            print(len(approx))
            x, y, w, h = cv2.boundingRect(approx)

            cv2.rectangle(img_contour, (x, y), (x+w, y+h), (0, 255, 0), 5)

            cv2.putText(img_contour, 'Points : ' + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img_contour, 'Area : ' + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img_contour, 'Mass Center  : ' + str((cX, cY)), (x + w + 20, y + h + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)


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

    imgStack = stackImage(0.8, ([img, imgGray, img_Canny], [img_dil, img_contour, img_contour]))

    cv2.imshow('Result', imgStack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break