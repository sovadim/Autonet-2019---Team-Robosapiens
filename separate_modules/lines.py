import cv2
import numpy as np
#import matplotlib.pyplot as plt

###################################################

# image parameters
im_height = 480 #
im_width = 640  #

# it's important to set up accurate roi cos the algoritm suggests
# calculating of average line so extra lines will spoil the result
l_roi_x = 0                     # X _|____ left  roi border
r_roi_x = im_width - l_roi_x    # X ____|_ right roi border
d_roi_y = im_height - 50        # Y ______ lower roi border
u_roi_y = 80                    # Y ------ upper roi border
u_roi_cnstr = 250
#

LINE_FOLLOW_CAM_INDEX = 0

###################################################

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(2/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)

    left_line = make_coordinates(image, left_fit_average)
    print('left line:', left_line)
    right_line = make_coordinates(image, right_fit_average)
    print('right line:', right_line)
    print()

    return np.array([left_line, right_line])

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # color to gray
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # optional
    canny = cv2.Canny(blur, 50, 150)  # gradient
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            # (255, 0, 0) - blue color
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

def region_of_interest(image):
    polygons = np.array([
        [(l_roi_x, im_height), (r_roi_x, im_height), (r_roi_x - u_roi_cnstr, u_roi_y), (l_roi_x + u_roi_cnstr, u_roi_y)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def play_image():
    filename = 'images/lines/challenge.jpg'

    image = cv2.imread(filename)

    lane_image = np.copy(image)
    canny_image = canny(lane_image)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(lane_image, lines)
    line_image = display_lines(lane_image, averaged_lines)
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
        canny_image = canny(frame)

        # area of frame where lines are supposed to be
        cropped_image = region_of_interest(canny_image)

        # getting lines
        lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)

        try:
            averaged_lines = average_slope_intercept(frame, lines)
            line_image = display_lines(frame, averaged_lines)
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
    cap = cv2.VideoCapture(LINE_FOLLOW_CAM_INDEX)

    while cap.isOpened():

        # getting frame
        _, frame = cap.read()

        # canny transform to prepare for detection
        canny_image = canny(frame)

        # area of frame where lines are supposed to be
        cropped_image = region_of_interest(canny_image)

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
                                precision_pixels, precision_degrees, threshold,
                                np.array([]), minLineLength, maxLineGap)



        try:
            averaged_lines = average_slope_intercept(frame, lines)
            line_image = display_lines(frame, averaged_lines)
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