cmake_minimum_required(VERSION 3.0.4)
project(test_robot_control)

find_package(catkin REQUIRED rospy)
#find_package(catkin REQUIRED hector_sensors_description)

catkin_package()

set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DOTHER_STUFF=1" )
