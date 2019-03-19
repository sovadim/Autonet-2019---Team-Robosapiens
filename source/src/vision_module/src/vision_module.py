#!/usr/bin/env python
import roslib; roslib.load_manifest('vision_module')
import rospy
from vision_info_msg.msg import vision_info_msg as vim
import settings as s
import cv2

def run():
    #pub = rospy.Publisher('vision_info', String, queue_size=10)
    pub = rospy.Publisher('vision_info', vim, queue_size=10)
    rospy.init_node('vision_module')

    cap = cv2.VideoCapture(0)

    while not rospy.is_shutdown():
        _, frame = cap.read()
        cv2.imshow('window', frame)

        str = "vision_module running"
        print("INFO " + str)
        #pub.publish(String(str))
        pub.publish(False, 0, False, 0, 0);
        #rospy.sleep(1.0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException: pass
