#!/usr/bin/env python
import roslib; roslib.load_manifest('vision_module')
import rospy
from vision_info_msg.msg import vision_info_msg as vim
import settings as s
import auxiliary_functions as aux
import numpy as np
import cv2

# init
pub = rospy.Publisher('vision_info', vim, queue_size=10)
rospy.init_node('vision_module')

# alignment buffers
light_buff = [0] * s.ALIGNMENT_BUFF_SIZE
sign_buff = [0] * s.ALIGNMENT_BUFF_SIZE
center_line_buff = [0] * s.LINES_ALIGNMENT_BUFF_SIZE
shift_line_buff = [0] * s.LINES_ALIGNMENT_BUFF_SIZE

line_center_x = 0
line_shift = 0
########################################################################
def get_average(buff, val):

    summ = 0

    # shift
    for i in range(0, len(buff) - 1):
        buff[i] = buff[i + 1]
        summ += buff[i]

    buff[len(buff) - 1] = val
    summ += val

    return summ//len(buff)
########################################################################
def get_frequent(buff, val):
    uniq_vals_buff = {}

    # shift
    for i in range(0, len(buff) - 1):
        buff[i] = buff[i + 1]

        if buff[i] in uniq_vals_buff.keys():
            uniq_vals_buff[buff[i]] += 1
        else:
            uniq_vals_buff[buff[i]] = 1
    buff[len(buff) - 1] = val

    # more frequent value search
    result = 0
    maxVal = 0

    for key, val in uniq_vals_buff.items():
        if val > maxVal:
            maxVal = val
            result = key

    return result
########################################################################
def send_message(light, sign=0, blocked=False, pos=0, shift=0):
    #pub.publish(False, 0, False, 0, 0);
    print(light, sign, blocked, pos, shift);
    pub.publish(light, sign, blocked, pos, shift);
########################################################################
def get_light(frame):
    # RED: True
    # Green: False
    RED = False

    # copy + canny
    copy = aux.canny(frame.copy())

    # contours searching
    contours = cv2.findContours(copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]

    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        cv2.drawContours(copy, contours, 0, (255, 0, 255), 5)

        (x, y, w, h) = cv2.boundingRect(contours[0])
        cv2.rectangle(copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

        image = frame[y:y + h, x:x + w]
        image = cv2.resize(image, (50, 100))
        #cv2.imshow('detected', image)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Getting the brightness component
        v = hsv[:, :, 2]

        red_sum = np.sum(v[0:35, 0:30])
        green_sum = np.sum(v[45:80, 0:30])

        area = cv2.contourArea(contours[0])

        if red_sum > green_sum and area > s.LIGHT_ENOUGH_AREA and (red_sum - green_sum) > s.LIGHT_ENOUGH_DIFFERENCE:
            RED = True

    cv2.imshow('result_light', copy)

    return get_frequent(light_buff, RED)
########################################################################
def get_sign(frame):
    sign = 0
    area = 0
    blocked = False

    #frameCopy = frame.copy()

    mask = cv2.inRange(frame, s.RED_BLUE_MASK, (255, 255, 255))
    #cv2.imshow('mask2', mask2)

    # contours searching
    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]

    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        cv2.drawContours(frame, contours, 0, (255, 0, 255), 5)

        (x, y, w, h) = cv2.boundingRect(contours[0])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        roImg = frame[y:y + h, x:x + w]
        roImg = cv2.resize(roImg, (s.size, s.size))
        roImg = cv2.inRange(roImg, s.RED_BLUE_MASK, (255, 255, 255))
        #cv2.imshow('detected', roImg)

        sign = aux.find_similar(roImg)

        #area = cv2.contourArea(contours[0])

    #cv2.imshow('result_sign', frame)

    sign = get_frequent(sign_buff, sign)

    if sign == 5:
        blocked = True

    return sign, area, blocked
########################################################################
def get_lines(frame):

    # canny transform and getting roi
    # we don't need to make frame copy at this step
    cropped_image = aux.region_of_interest(aux.canny(frame))
    cv2.imshow('cropped', cropped_image)
    # getting lines

    # required accuracy settings
    # we are forced to lower accuracy for a more stable result
    # so in comments are proposed default values
    precision_pixels = 5  # 2
    precision_degrees = np.pi / 90  # np.pi / 180
    minLineLength = 40  # 40
    maxLineGap = 5  # 5
    threshold = 50  # 100 mush number gives more smooth result but can lost the image at all
    # ------------------------------------------------------ #
    lines = cv2.HoughLinesP(cropped_image,
                            precision_pixels,
                            precision_degrees,
                            threshold,
                            np.array([]),
                            minLineLength,
                            maxLineGap)

    try:
        # average_lines: [left_line, right_line]
        # line: [x1, y1, x2, y2]
        averaged_lines = aux.average_slope_intercept(frame, lines)

        line_image = aux.display_lines(frame, averaged_lines)
        combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

        # getting center line
        #cv2.rectangle(combo_image, (averaged_lines[0][0], 0), (averaged_lines[1][0], s.im_height), (255, 0, 255), 5)
        line_center_x = get_average(center_line_buff, averaged_lines[0][0] + (averaged_lines[1][0] - averaged_lines[0][0])//2)

        cv2.rectangle(combo_image, (line_center_x - 2, 0), (line_center_x + 2, s.im_height), (255, 255, 0), 5)

        # getting shift from forward direction
        #cv2.rectangle(combo_image, (x2_l, 0), (x2_r, s.im_height), (255, 0, 0), 5)
        line_shift = get_average(shift_line_buff, averaged_lines[0][2] + (averaged_lines[1][2] - averaged_lines[0][2]) // 2)

        cv2.rectangle(combo_image, (line_shift - 2, 0), (line_shift + 2, s.im_height), (0, 255, 255), 5)

        # end data
        line_shift = line_center_x - line_shift
        line_center_x -= s.im_width//2

        cv2.imshow('result_lines', combo_image)
    except:
        cv2.imshow('result_lines', frame)
        line_center_x = get_average(center_line_buff, 0)
        line_shift = get_average(shift_line_buff, 0)

    #cv2.imshow('cropped', cropped_image)

    line_center_x = line_center_x * 100 // s.im_width
    line_shift = line_shift * 100 // s.im_width

    #print(line_center_x, line_shift)

    return line_center_x, line_shift
########################################################################
def run():
    cap_1 = cv2.VideoCapture(s.SIGN_CHECK_CAM_INDEX)
    cap_2 = cv2.VideoCapture(s.LINE_FOLLOW_CAM_INDEX)

    while not rospy.is_shutdown():
        light = False
        light_area = 0
        sign = 0
        sign_area = 0
        blocked = False

        _1, frame1 = cap_1.read()
        _2, frame2 = cap_2.read()

        # TRAFFIC LIGHT
        light = get_light(frame1)

        if light:
            send_message(light, 0, False, 0, 0)
            continue

        # SIGN
        sign, sign_area, blocked = get_sign(frame1)

        if sign_area > s.SIGN_ENOUGH_AREA:
            send_message(light, sign, blocked)
            continue

        # LINES
        line_center_x, line_shift = get_lines(frame2)

        # MESSAGE
        send_message(light, sign, blocked, line_center_x, line_shift)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_1.release()
    cap_2.release()
    cv2.destroyAllWindows()
########################################################################
if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException: pass
########################################################################
