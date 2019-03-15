import cv2
import numpy as np

###################################################

#
LINE_FOLLOW_CAM_INDEX = 1

# Sample images for comparison
SIGN_FORWARD = cv2.imread('images/signs/fw.jpg')
SIGN_LEFT = cv2.imread('images/signs/left.jpg')
SIGN_RIGHT = cv2.imread('images/signs/right.jpg')
SIGN_FORWARD_AND_LEFT = cv2.imread('images/signs/fw_le.jpg')
SIGN_FORWARD_AND_RIGHT = cv2.imread('images/signs/fw_ri.jpg')
SIGN_BLOCK = cv2.imread('images/signs/block.jpg')

# The larger the picture the more accurate the result
# but the lower the processing speed
size = 64
SIGN_FORWARD = cv2.resize(SIGN_FORWARD, (size, size))
SIGN_LEFT = cv2.resize(SIGN_LEFT, (size, size))
SIGN_RIGHT = cv2.resize(SIGN_RIGHT, (size, size))
SIGN_FORWARD_AND_LEFT = cv2.resize(SIGN_FORWARD_AND_LEFT, (size, size))
SIGN_FORWARD_AND_RIGHT = cv2.resize(SIGN_FORWARD_AND_RIGHT, (size, size))
SIGN_BLOCK = cv2.resize(SIGN_BLOCK, (size, size))

# Mask
#RED_BLUE_MASK = (150, 91, 90)
RED_BLUE_MASK = (89, 124, 73)

# Image binarization
SIGN_FORWARD = cv2.inRange(SIGN_FORWARD, RED_BLUE_MASK, (255, 255, 255))
SIGN_LEFT = cv2.inRange(SIGN_LEFT, RED_BLUE_MASK, (255, 255, 255))
SIGN_RIGHT = cv2.inRange(SIGN_RIGHT, RED_BLUE_MASK, (255, 255, 255))
SIGN_FORWARD_AND_LEFT = cv2.inRange(SIGN_FORWARD_AND_LEFT, RED_BLUE_MASK, (255, 255, 255))
SIGN_FORWARD_AND_RIGHT = cv2.inRange(SIGN_FORWARD_AND_RIGHT, RED_BLUE_MASK, (255, 255, 255))
SIGN_BLOCK = cv2.inRange(SIGN_BLOCK, RED_BLUE_MASK, (255, 255, 255))

# Here we will collect numbers of similar pixels by detected and sample image
COINCIDENCES = ([0] * 6)

# Number of similar pixels in matrix to conclude the sign is recognized
ENTRY_THRESHOLD = 3000

###################################################

def find_similar(image):

    # Summ number of similar pixels
    for i in range(size):
        for j in range(size):
            if image[i][j] == SIGN_FORWARD[i][j]:
                COINCIDENCES[0] += 1
            if image[i][j] == SIGN_LEFT[i][j]:
                COINCIDENCES[1] += 1
            if image[i][j] == SIGN_RIGHT[i][j]:
                COINCIDENCES[2] += 1
            if image[i][j] == SIGN_FORWARD_AND_LEFT[i][j]:
                COINCIDENCES[3] += 1
            if image[i][j] == SIGN_FORWARD_AND_RIGHT[i][j]:
                COINCIDENCES[4] += 1
            if image[i][j] == SIGN_BLOCK[i][j]:
                COINCIDENCES[5] += 1

    # Searching for maximum coincidence
    maxVal = 0
    maxInd = 0

    for i in range(len(COINCIDENCES)):
        if COINCIDENCES[i] > maxVal:
            maxVal = COINCIDENCES[i]
            maxInd = i

    if maxVal > ENTRY_THRESHOLD:
        if maxInd == 0:
            return 'SIGN_FORWARD'
        elif maxInd == 1:
            return 'SIGN_LEFT'
        elif maxInd == 2:
            return 'SIGN_RIGHT'
        elif maxInd == 3:
            return 'SIGN_FORWARD_AND_LEFT'
        elif maxInd == 4:
            return 'SIGN_FORWARD_AND_RIGHT'
        elif maxInd == 5:
            return 'SIGN_BLOCK'

    #print(COINCIDENCES)

    for i in range(len(COINCIDENCES)):
        COINCIDENCES[i] = 0

def play_webcam():
    cap = cv2.VideoCapture(LINE_FOLLOW_CAM_INDEX)

    while cap.isOpened():

        # getting frame
        _, frame = cap.read()

        frameCopy = frame.copy()

        # hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # avoiding of color noises
        hsv = cv2.blur(hsv, (5, 5))

        # mask
        mask = cv2.inRange(hsv, RED_BLUE_MASK, (255, 255, 255))

        # - noises
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=4)

        # contours searching
        contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = contours[0]
        cv2.imshow('mask', mask)
        if contours:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            cv2.drawContours(frame, contours, 0, (255, 0, 255), 5)

            (x, y, w, h) = cv2.boundingRect(contours[0])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            roImg = frameCopy[y:y+h, x:x+w]
            roImg = cv2.resize(roImg, (size, size))
            roImg = cv2.inRange(roImg, (89, 124, 73), (255, 255, 255))
            #cv2.imshow('detected', roImg)

            print(find_similar(roImg))

        cv2.imshow('result', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

play_webcam()

print("It's the end of the world")