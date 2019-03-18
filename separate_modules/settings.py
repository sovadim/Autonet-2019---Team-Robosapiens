import cv2

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

LINE_FOLLOW_CAM_INDEX = 2
SIGN_CHECK_CAM_INDEX = 0

# Mask
#RED_BLUE_MASK = (150, 91, 90)
RED_BLUE_MASK = (89, 124, 73)

# Sample images for comparison
# The larger the picture the more accurate the result
# but the lower the processing speed
size = 64
SIGN_FORWARD = cv2.resize(cv2.imread('images/signs/fw.jpg'), (size, size))
SIGN_LEFT = cv2.resize(cv2.imread('images/signs/left.jpg'), (size, size))
SIGN_RIGHT = cv2.resize(cv2.imread('images/signs/right.jpg'), (size, size))
SIGN_FORWARD_AND_LEFT = cv2.resize(cv2.imread('images/signs/fw_le.jpg'), (size, size))
SIGN_FORWARD_AND_RIGHT = cv2.resize(cv2.imread('images/signs/fw_ri.jpg'), (size, size))
SIGN_BLOCK = cv2.resize(cv2.imread('images/signs/block.jpg'), (size, size))

# Image binarization
SIGN_FORWARD = cv2.inRange(SIGN_FORWARD, RED_BLUE_MASK, (255, 255, 255))
SIGN_LEFT = cv2.inRange(SIGN_LEFT, RED_BLUE_MASK, (255, 255, 255))
SIGN_RIGHT = cv2.inRange(SIGN_RIGHT, RED_BLUE_MASK, (255, 255, 255))
SIGN_FORWARD_AND_LEFT = cv2.inRange(SIGN_FORWARD_AND_LEFT, RED_BLUE_MASK, (255, 255, 255))
SIGN_FORWARD_AND_RIGHT = cv2.inRange(SIGN_FORWARD_AND_RIGHT, RED_BLUE_MASK, (255, 255, 255))
SIGN_BLOCK = cv2.inRange(SIGN_BLOCK, RED_BLUE_MASK, (255, 255, 255))

# Number of similar pixels in matrix to conclude the sign is recognized
ENTRY_THRESHOLD = 3000

# TRAFFIC LIGHT

#RED_GREEN = cv2.imread('images/traffic_lights/red_green.jpg')
RED = cv2.imread('images/traffic_lights/red.jpg')
GREEN = cv2.imread('images/traffic_lights/green.jpg')

IMAGES = [RED, GREEN]

# TODO: calculate
SIGN_ENOUGH_AREA = 10000
# TODO: calculate
LIGHT_ENOUGH_AREA = 70000
LIGHT_ENOUGH_DIFFERENCE = 20000

RED_LIGHT = True

###################################################