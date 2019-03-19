# Support program for mask search

import cv2

def do_nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('mask')

cv2.createTrackbar('minb', 'mask', 0, 255, do_nothing)
cv2.createTrackbar('ming', 'mask', 0, 255, do_nothing)
cv2.createTrackbar('minr', 'mask', 0, 255, do_nothing)

cv2.createTrackbar('maxb', 'mask', 0, 255, do_nothing)
cv2.createTrackbar('maxg', 'mask', 0, 255, do_nothing)
cv2.createTrackbar('maxr', 'mask', 0, 255, do_nothing)

while cap.isOpened():
    _, frame = cap.read()

    minb = cv2.getTrackbarPos('minb', 'mask')
    ming = cv2.getTrackbarPos('ming', 'mask')
    minr = cv2.getTrackbarPos('minr', 'mask')

    maxb = cv2.getTrackbarPos('maxb', 'mask')
    maxg = cv2.getTrackbarPos('maxg', 'mask')
    maxr = cv2.getTrackbarPos('maxr', 'mask')

    mask = cv2.inRange(frame, (minb, ming, minr), (maxb, maxg, maxr))
    cv2.imshow('mask', mask)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('mask', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
