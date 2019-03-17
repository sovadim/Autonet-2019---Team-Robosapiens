import cv2
import numpy as np
import time
from separate_modules import settings as s
from separate_modules import auxiliary_functions as aux


def play_webcam():
    cap = cv2.VideoCapture(s.LINE_FOLLOW_CAM_INDEX)

    while cap.isOpened():
        #print(cv2.CAP_PROP_FPS)
        # getting frame
        _, frame = cap.read()

        frameCopy = frame.copy()

        # hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # avoiding of color noises
        hsv = cv2.blur(hsv, (5, 5))

        # mask
        mask = cv2.inRange(hsv, s.RED_BLUE_MASK, (255, 255, 255))

        # minus noises
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=4)

        # contours searching
        contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = contours[0]
        #cv2.imshow('mask', mask)
        if contours:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            cv2.drawContours(frame, contours, 0, (255, 0, 255), 5)

            (x, y, w, h) = cv2.boundingRect(contours[0])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            roImg = frameCopy[y:y+h, x:x+w]
            roImg = cv2.resize(roImg, (st.size, st.size))
            roImg = cv2.inRange(roImg, (89, 124, 73), (255, 255, 255))
            #cv2.imshow('detected', roImg)

            print(aux.find_similar(roImg))

        cv2.imshow('result', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

play_webcam()

print("It's the end of the world")