#!/usr/bin/env python2
import rospy
import actionlib
import irob_assignment_1.msg
from irob_assignment_1.srv import GetSetpoint, GetSetpointRequest, GetSetpointResponse
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path
import tf2_ros
import tf2_geometry_msgs
from math import atan2, hypot, sqrt

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

# Max linear velocity (m/s)
max_linear_velocity = 0.5
# Max angular velocity (rad/s)
max_angular_velocity = 1.0


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
    # Call service client with path

    # Transform Setpoint from service client

    # Create Twist message from the transformed Setpoint

    # Publish Twist

    # Call service client again if the returned path is not empty and do stuff again

    # Send 0 control Twist to stop robot

    # Get new path from action server

def stopMovement():
    twistMsg = Twist()
    twistMsg.linear.x =0
    twistMsg.linear.y = 0
    twistMsg.linear.z = 0
    twistMsg.angular.x = 0
    twistMsg.angular.y = 0
    twistMsg.angular.z = 0
    
    pub.publish(twistMsg)

def get_path():
    rospy.loginfo("trying to get path")
    global goal_client
    goal_client = irob_assignment_1.msg.GetNextGoalActionGoal()
    client = actionlib.SimpleActionClient('get_next_goal', irob_assignment_1.msg.GetNextGoalAction)

    client.wait_for_server()
    client.send_goal(goal_client)
    client.wait_for_result()
    # Get path from action server
    path = client.get_result()
    rospy.loginfo("Got result")
    #rospy.loginfo("path %s", path)
    rospy.loginfo("gain %s", path.gain)
    # Call move with path from action server
    return path

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

if __name__ == "__main__":
    # Init node
    rospy.init_node("controller")
    rospy.loginfo("node initiated")
    global tfBuffer
    tfBuffer = tf2_ros.Buffer()
    global listener
    listener = tf2_ros.TransformListener(tfBuffer)
    
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    
    done = False
    while not done:
        stopMovement()
        p = get_path()
        path = p.path
        if len(path.poses) == 0:
               exit()
        rate = rospy.Rate(10.0)
        while len(path.poses) != 0:
            rospy.loginfo("in while")
            setPointResponse = get_setpoint(path)
            rospy.loginfo("got setpointResponse")
            path = setPointResponse.new_path
            rospy.loginfo("got new path")
            transformedSetpoint = transformSetPoint(setPointResponse)
            if transformedSetpoint is None:
                exit("failure when transforming set point")
            rospy.loginfo("got transformed setpoint")
            move(transformedSetpoint)
            rospy.loginfo("moved")
            rate.sleep()

        
    # Init publisher
    
    
    # Init simple action server

    # Init service client

    # Call get path

    # Spin
    rospy.spin()