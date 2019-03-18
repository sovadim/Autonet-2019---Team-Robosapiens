import cv2
import numpy as np
from separate_modules import settings as s

# LINES

def canny(image):
    #gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # color to gray
    #blur = cv2.GaussianBlur(gray, (5, 5), 0)  # optional
    #return cv2.Canny(blur, 50, 150)  # gradient

    # optimize
    return cv2.Canny(cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), (5, 5), 0), 50, 150)

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
    #print('left line:', left_line)
    right_line = make_coordinates(image, right_fit_average)
    #print('right line:', right_line)
    #print()

    return np.array([left_line, right_line])


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            # (255, 0, 0) - blue color
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

def region_of_interest(image):
    polygons = np.array([
        [(s.l_roi_x, s.im_height),
         (s.r_roi_x, s.im_height),
         (s.r_roi_x - s.u_roi_cnstr, s.u_roi_y),
         (s.l_roi_x + s.u_roi_cnstr, s.u_roi_y)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

# SIGNS
def find_similar(image):

    # Here we will collect numbers of similar pixels by detected and sample image
    COINCIDENCES = ([0] * 6)

    # Summ number of similar pixels
    for i in range(s.size):
        for j in range(s.size):
            if image[i][j] == s.SIGN_FORWARD[i][j]:
                COINCIDENCES[0] += 1
            if image[i][j] == s.SIGN_LEFT[i][j]:
                COINCIDENCES[1] += 1
            if image[i][j] == s.SIGN_RIGHT[i][j]:
                COINCIDENCES[2] += 1
            if image[i][j] == s.SIGN_FORWARD_AND_LEFT[i][j]:
                COINCIDENCES[3] += 1
            if image[i][j] == s.SIGN_FORWARD_AND_RIGHT[i][j]:
                COINCIDENCES[4] += 1
            if image[i][j] == s.SIGN_BLOCK[i][j]:
                COINCIDENCES[5] += 1

    # Searching for maximum coincidence
    maxVal = 0
    maxInd = 0

    for i in range(len(COINCIDENCES)):
        if COINCIDENCES[i] > maxVal:
            maxVal = COINCIDENCES[i]
            maxInd = i

    return maxInd

    #print(COINCIDENCES)