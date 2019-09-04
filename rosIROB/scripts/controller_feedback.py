#!/usr/bin/env python2
import rospy
import actionlib
import irob_assignment_1.msg
from irob_assignment_1.srv import GetSetpoint, GetSetpointRequest, GetSetpointResponse
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path
import tf2_ros
import tf2_geometry_msgs
from math import atan2, hypot

# Use to transform between frames
tf_buffer = None
listener = None

# The exploration simple action client
goal_client = None
# The collision avoidance service client
control_client = None
# The velocity command publisher
pub = None

# The robots frame
robot_frame_id = "base_link"

# Min allowed gain to move along path (in feedback)
min_allowed_gain = 3

# Max linear velocity (m/s)
max_linear_velocity = 0.5
# Max angular velocity (rad/s)
max_angular_velocity = 1.0


def goal_active():
    rospy.loginfo("I got activated")


def goal_feedback(feedback):
    rospy.loginfo("I got feedback")

    # Check if this path has higher gain than min_allowed_gain

    # If it has cancel goal and move along the path


def goal_result(state, result):
    rospy.loginfo("I got a result")

    # If the state is succeeded then

    # Move along the path if path is not empty


def move(point):
    global control_client, robot_frame_id, pub

    


    twistMsg = Twist()
    twistMsg.linear.x = 0.5 * sqrt(point.x ** 2 + point.y ** 2)
    twistMsg.linear.y = 0
    twistMsg.linear.z = 0
    twistMsg.angular.x = 0
    twistMsg.angular.y = 0
    twistMsg.angular.z = 4 * atan2(point.y, point.x)
    if (twistMsg.angular.z >1):
        twistMsg.angular.z = 1
    
    if (twistMsg.linear.x >0.5):
        twistMsg.linear.x = 0.5
    
    pub.publish(twistMsg)
    rospy.loginfo("linear.x %s angular.z %s", twistMsg.linear.x, twistMsg.angular.z)

def stopMovement():
    twistMsg = Twist()
    twistMsg.linear.x =0
    twistMsg.linear.y = 0
    twistMsg.linear.z = 0
    twistMsg.angular.x = 0
    twistMsg.angular.y = 0
    twistMsg.angular.z = 0    
    pub.publish(twistMsg)

def get_setpoint(path):
    rospy.wait_for_service("get_setpoint")
    try:
        setPointProxy = rospy.ServiceProxy("get_setpoint", GetSetpoint)
        setPointResponse = setPointProxy(path)
        return setPointResponse
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def transformSetPoint(setPointResponse):
    
    try:
        rospy.loginfo("trying to transform from source %s to target %s", setPointResponse.setpoint.header.frame_id, "base_link")
        trans = tfBuffer.lookup_transform("base_link", setPointResponse.setpoint.header.frame_id, setPointResponse.setpoint.header.stamp)
        
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        rospy.logerr("transformation went wront")
        return None
    
    return tf2_geometry_msgs.do_transform_point(setPointResponse.setpoint, trans).point


def get_path():
    global goal_client

    # Get path from action server

    # Call move with path from action server


if __name__ == "__main__":
    # Init node

    # Init publisher

    # Init simple action server

    # Init service client

    # Call get path

    # Spin
