import cv2
from separate_modules import settings as s
from separate_modules import auxiliary_functions as aux

def send_message(light, sign=0, block=False, pos=0, angle=0):
    print('msg: [', light, ',', sign, ',', block, ',', pos, ',', angle, ']')
    # TODO: creating and sending message
    pass

def get_light():
    # TODO: light recognition
    # RED: True
    # Green: False
    RED = False
    area = 0

    return RED, area

def get_sign():
    # TODO: getting sign
    sign = 1
    area = 5000
    blocked = True

    return sign, area, blocked

def get_lines():
    # TODO: getting lines info
    # TODO: align lines in additional function
    pos = 0
    angle = 0

    return pos, angle

def run():
    cap_1 = cv2.VideoCapture(s.SIGN_CHECK_CAM_INDEX)
    #cap_2 = cv2.VideoCapture(s.LINE_FOLLOW_CAM_INDEX)

    while True:
        _1, frame1 = cap_1.read()
        #_2, frame2 = cap_2.read()

        cv2.imshow('1', frame1)
        #cv2.imshow('2', frame2)

        # TRAFFIC LIGHT
        light, light_area = get_light()

        if light:
            send_message(light, 0, False, 0, 0)
            continue

        # SIGN
        sign, sign_area, blocked = get_sign()

        if sign_area > s.SIGN_ENOUGH_AREA:
            send_message(light, sign, blocked)
            continue

        # LINES
        pos, angle = get_lines()

        # MESSAGE
        send_message(light, sign, blocked, pos, angle)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_1.release()
    #cap_2.release()

    cv2.destroyAllWindows()

run()

print("It's the end of the world")