#!/usr/bin/env python
import roslib; roslib.load_manifest('vision_module')
import rospy
from std_msgs.msg import String
import settings as s

def run():
    pub = rospy.Publisher('vision_info', String, queue_size=10)
    rospy.init_node('vision_module')

    while not rospy.is_shutdown():
        str = "vision_module running"
        print("INFO " + str + s.msg)
        pub.publish(String(str))
        rospy.sleep(1.0)

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException: pass
