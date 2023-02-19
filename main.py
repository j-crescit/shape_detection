import cv2
import numpy as np

cap = cv2.VideoCapture(1)

def empty(pos):
    pass

cv2.namedWindow('Parameters')
cv2.resizeWindow('Parameters', 600, 300)
cv2.createTrackbar('Threshold_1', 'Parameters', 0, 255, empty)
cv2.createTrackbar('Threshold_2', 'Parameters', 0, 255, empty)
cv2.createTrackbar("Area", "Parameters", 1000, 5000, empty)

def stack_img(scale, img_array):
    rows = len(img_array)
    cols = len(img_array[0])

    rows_available = isinstance(img_array[0], list)

    width = img_array[0][0].shape[1]
    height = img_array[0][0].shape[0]

    if rows_available:
        for x in range(0, rows):

            for y in range(0, cols):

                if img_array[x][y].shape[:2] == img_array[0][0].shape[:2]:
                    img_array[x][y] = cv2.resize(img_array[x][y], (0, 0), None, scale, scale)

                else:
                    img_array[x][y] = cv2.resize(img_array[x][y], (img_array[0][0].shape[1], img_array[0][0].shape[0]), None, scale, scale)

                if len(img_array[x][y].shape) == 2:
                    img_array[x][y] = cv2.cvtColor(img_array[x][y], cv2.COLOR_GRAY2BGR)

        img_blank = np.zeros((height, width, 3), np.uint8)

        hor = [img_blank]*rows
        hor_con = [img_blank]*rows

        for x in range(0, rows):
            hor[x] = np.hstack(img_array[x])

        ver = np.vstack(hor)

    else:
        for x in range(0, rows):

            if img_array[x].shape[:2] == img_array[0].shape[:2]:
                img_array[x] = cv2.resize(img_array[x], (0, 0), None, scale, scale)

            else:
                img_array[x] = cv2.resize(img_array[x], (img_array[0].shape[1], img_array[0].shape[0]), None, scale, scale)

            if len(img_array[x].shape) == 2:
                img_array[x] = cv2.cvtColor(img_array[x], cv2.COLOR_GRAY2BGR)

        hor = np.hstack(img_array)
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

        y_list=[]

        y_list.append(abs(360 - cY))

        amplitude = round(abs(360-cY)/94.2, 3)
        max_amplitude = round(max(y_list)/94.2, 3)

        cv2.circle(img_contour, (cX, cY), 4, (255, 0, 0), -1)
        cv2.drawContours(img_contour, [i], 0, (0, 255, 255), 2)

        if area > area_min:
            cv2.drawContours(img_contour, i, -1, (255, 0, 255), 7)

            arc = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * arc, True)

            x, y, w, h = cv2.boundingRect(approx)

            cv2.rectangle(img_contour, (x, y), (x+w, y+h), (0, 255, 0), 5)

            cv2.putText(img_contour, 'Points : ' + str(len(approx)), (20, 40), cv2.FONT_HERSHEY_COMPLEX, 0.75, (212, 175, 55), 1)
            cv2.putText(img_contour, 'Amplitude : ' + str(amplitude) + 'mm', (20, 75), cv2.FONT_HERSHEY_COMPLEX, 0.75, (212, 175, 55), 1)
            cv2.putText(img_contour, 'Max Amplitude : ' + str(max_amplitude) + 'mm', (20, 110), cv2.FONT_HERSHEY_COMPLEX, 0.75, (212, 175, 55), 1)

while True:
    success, img = cap.read()
    img_contour = img.copy()

    img_blur = cv2.GaussianBlur(img, (7, 7), 1)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

    threshold_1 = cv2.getTrackbarPos('Threshold_1', 'Parameters')
    threshold_2 = cv2.getTrackbarPos('Threshold_2', 'Parameters')

    img_canny = cv2.Canny(img_gray, threshold_1, threshold_2)
    kernel = np.ones((5, 5))
    img_dil = cv2.dilate(img_canny, kernel, iterations = 1)

    getContours(img_dil, img_contour)

    stack = stack_img(0.7, ([img, img_blur, img_gray], [img_canny, img_dil, img_contour]))

    cv2.imshow('Result', stack)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

