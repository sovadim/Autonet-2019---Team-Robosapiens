#!/usr/bin/env python
import roslib; roslib.load_manifest('vision_module')
import rospy
from vision_info_msg.msg import vision_info_msg as vim
import settings as s


def run():
    #pub = rospy.Publisher('vision_info', String, queue_size=10)
    pub = rospy.Publisher('vision_info', vim, queue_size=10)
    rospy.init_node('vision_module')

    while not rospy.is_shutdown():
        str = "vision_module running"
        print("INFO " + str)
        #pub.publish(String(str))
        pub.publish(False, 0, False, 0, 0);
        rospy.sleep(1.0)

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException: pass
