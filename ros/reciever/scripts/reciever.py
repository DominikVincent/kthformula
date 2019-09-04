#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt32,Float32

def callback(data):
    newData = data.data / 0.15
    pub.publish(newData)

if __name__ == "__main__":
    rospy.init_node("reciever")
    rospy.Subscriber("/Hollidt", UInt32, callback)
    global pub
    pub = rospy.Publisher("/kthfs/result", Float32, queue_size=10)
    
    rospy.spin()