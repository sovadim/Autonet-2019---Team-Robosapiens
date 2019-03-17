import cv2
import numpy as np
from separate_modules import settings as s
from separate_modules import auxiliary_functions as aux
#import matplotlib.pyplot as plt

def play_image():
    filename = 'images/lines/challenge.jpg'

    image = cv2.imread(filename)

    lane_image = np.copy(image)
    canny_image = aux.canny(lane_image)
    cropped_image = aux.region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = aux.average_slope_intercept(lane_image, lines)
    line_image = aux.display_lines(lane_image, averaged_lines)
    combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)

    cv2.imshow('result', combo_image)
    #plt.imshow(combo_image)
    #plt.show()
    cv2.waitKey(0)

def play_video():
    filename = 'videos/test.mp4'

    cap = cv2.VideoCapture(filename)

    while cap.isOpened():
        # getting frame
        _, frame = cap.read()

        # canny transform to prepare for detection
        canny_image = aux.canny(frame)

        # area of frame where lines are supposed to be
        cropped_image = aux.region_of_interest(canny_image)

        # getting lines
        lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)

        try:
            averaged_lines = aux.average_slope_intercept(frame, lines)
            line_image = aux.display_lines(frame, averaged_lines)
            combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

            cv2.imshow('result', combo_image)
        except:
            cv2.imshow('result', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # we must close video stream
    cap.release()
    cv2.destroyAllWindows()

def play_webcam():
    cap = cv2.VideoCapture(s.LINE_FOLLOW_CAM_INDEX)

    while cap.isOpened():

        # getting frame
        _, frame = cap.read()

        # canny transform to prepare for detection
        canny_image = aux.canny(frame)

        # area of frame where lines are supposed to be
        cropped_image = aux.region_of_interest(canny_image)

        # getting lines

        # required accuracy settings
        # we are forced to lower accuracy for a more stable result
        # so in comments are proposed default values
        precision_pixels = 5 #2
        precision_degrees = np.pi / 90 #np.pi / 180
        minLineLength = 40 #40
        maxLineGap = 5 #5
        threshold = 50 # 100 mush number gives more smooth result but can lost the image at all
        # ------------------------------------------------------ #
        lines = cv2.HoughLinesP(cropped_image,
                                precision_pixels,
                                precision_degrees,
                                threshold,
                                np.array([]),
                                minLineLength,
                                maxLineGap)

        try:
            averaged_lines = aux.average_slope_intercept(frame, lines)
            line_image = aux.display_lines(frame, averaged_lines)
            combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
            cv2.imshow('result', combo_image)
        except:
            cv2.imshow('result', frame)

        cv2.imshow('cropped', cropped_image)

        #plt.imshow(canny_image)
        #plt.show(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#play_image()
#play_video()
play_webcam()

print("It's the end of the world")