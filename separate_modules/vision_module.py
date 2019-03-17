import cv2
from separate_modules import settings as s
from separate_modules import auxiliary_functions as aux

def send_message():
    # TODO: creating and sending message
    pass

def run():
    cap_1 = cv2.VideoCapture(s.LINE_FOLLOW_CAM_INDEX)
    cap_2 = cv2.VideoCapture(s.SIGN_CHECK_CAM_INDEX)

    while True:
        # TODO: light recognition

        # TODO: getting sign

        # TODO: getting lines info

        # TODO: sending message

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_1.release()
    cap_2.release()

    cv2.destroyAllWindows()

run()

print("It's the end of the world")