import cv2


while True:
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()