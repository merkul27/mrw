#!/usr/bin/env python3

import math
import random

import rospy

from geometry_msgs.msg import PoseStamped
from gazebo_msgs.msg import ModelStates 

robot_x = None
robot_y = None
robot_ori = None

def cb_robot_pos(msg):
    global robot_x   
    global robot_y
    global robot_ori
    # get index
    if 'test_robot' not in msg.name:
        return
    ind = msg.name.index('test_robot')
    # read data
    robot_x = msg.pose[ind].position.x
    robot_y = msg.pose[ind].position.y
    robot_ori = 2*math.atan2(msg.pose[ind].orientation.z,
                             msg.pose[ind].orientation.w)
    #rospy.loginfo('Pos: {} {} {}'.format(robot_x, robot_y, robot_ori))

if __name__ == '__main__':
    # connect to roscore
    rospy.init_node('move_node')
    # create ROS infrastructure
    output_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
    input_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, cb_robot_pos)
    #rospy.sleep(5.)
    while True:
        rospy.sleep(2.)
        # create goal
        gx = random.random()*4 - 2
        gy = random.random()*4 - 2
        g_ori = random.random()*2*math.pi - math.pi
        rospy.loginfo('Goal pos: {:.2f} {:.2f} {:.2f}'.format(gx, gy, g_ori))
        # create output message
        output_msg = PoseStamped()
        output_msg.header.frame_id = 'map'
        output_msg.pose.position.x = gx
        output_msg.pose.position.y = gy
        output_msg.pose.orientation.z = math.sin(0.5 * g_ori)
        output_msg.pose.orientation.w = math.cos(0.5 * g_ori)
        # send message
        output_pub.publish(output_msg)
        while True:
            rospy.sleep(1)
            #rospy.loginfo('Current pos: {:.2f} {:.2f} {:.2f}'.format(robot_x, robot_y, robot_ori))
            if abs(gx - robot_x) < 0.3 and abs(gy - robot_y) < 0.3:
                rospy.loginfo('Reached goal: {:.2f} {:.2f} {:.2f}'.format(robot_x, robot_y, robot_ori))
                break
