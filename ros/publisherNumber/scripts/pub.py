#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt32




if __name__ == '__main__':
    rospy.init_node("hollidt_publisher")
    global pub
    pub = rospy.Publisher("/Hollidt", UInt32, queue_size=10)
    n = 4
    k = 0
    rate = rospy.Rate(20000)
    while not rospy.is_shutdown():
        
        pub.publish(k)
        k += n
        
        try:
            rate.sleep()
        except rospy.ROSInterruptException:
            exit()