import cv2
import numpy as np

#RED_GREEN = cv2.imread('images/traffic_lights/red_green.jpg')
RED = cv2.imread('images/traffic_lights/red.jpg')
GREEN = cv2.imread('images/traffic_lights/green.jpg')

IMAGES = [RED, GREEN]

for i in range(len(IMAGES)):
    #cv2.imshow('window' + str(i), IMAGES[i])

    cutedImage = IMAGES[i][10:90, 10:40]
    cv2.imshow(str(i), cutedImage)

    hsv = cv2.cvtColor(cutedImage, cv2.COLOR_BGR2HSV)

    # Getting the brightness component
    v = hsv[:, :, 2]
    cv2.imshow("v" + str(i), v)

    red_sum = np.sum(v[0:35, 0:30])
    green_sum = np.sum(v[45:80, 0:30])

    # visual check
    #cv2.rectangle(cutedImage, (0, 0), (30, 30), (0, 0, 255), 3)
    #cv2.rectangle(cutedImage, (0, 47), (30, 77), (0, 255, 0), 3)
    #cv2.imshow(str(i), cutedImage)
    #print('red:', red_sum, '\ngreen:', green_sum)

    if red_sum > green_sum:
        print('red')
    else:
        print('green')

    key = cv2.waitKey()


cv2.destroyAllWindows()