#!/usr/bin/env python3
from turtle import position
import rospy
import numpy
import math
import tf
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Pose
from sensor_msgs.msg import Range # Message type used in the node

# initialize node
rospy.init_node('merge_maps')

robot_pose = tf.TransformListener()

rate = rospy.Rate(10) # 1 Hz

map_msg_map = OccupancyGrid()
map_msg_gmap = OccupancyGrid()
merged_map = OccupancyGrid()
merged_map.header.frame_id = 'merged_map'
resolution = 0.025
width = 800
height = 800

def sub_callback_gmapping(msg):
    #rospy.loginfo("Front sensor range: %f", msg.range)
    global map_msg_gmap
    map_msg_gmap = msg

def sub_callback_mapping(msg):
    #rospy.loginfo("Left sensor range: %f", msg.range)
    global map_msg_map
    map_msg_map = msg

# rospy.init_node('subscriber_py') # Init the node with name "subscriber_py"

rospy.Subscriber("robot/map", OccupancyGrid, sub_callback_mapping, queue_size=10)
rospy.Subscriber("map", OccupancyGrid, sub_callback_gmapping, queue_size=10)

# Publishers
merge_pub = rospy.Publisher("/merged/map", OccupancyGrid, queue_size = 10)

rospy.loginfo("subscriber.py node has started and subscribed to sensor/ir_*** topics")

# rospy.spin()

# main function
if __name__ == '__main__':

    # fill map_msg with the parameters from launchfile
    merged_map.info.resolution = resolution
    merged_map.info.width = width
    merged_map.info.height = height
    merged_map.data = list(range(width*height))

    merged_map.info.origin.position.x = - width // 2 * resolution
    merged_map.info.origin.position.y = - height // 2 * resolution

    '''
    # set grid parameters
    if rospy.has_param("occupancy_rate"):
        rate = rospy.get_param("occupancy_rate")

    if rospy.has_param("grid_resolution"):
        resolution = rospy.get_param("grid_resolution")

    if rospy.has_param("grid_width"):
        width = rospy.get_param("grid_width")

    if rospy.has_param("grid_height"):
        height = rospy.get_param("grid_height")
    '''
    while not rospy.is_shutdown():
        
		# build ros map message and publish
        print(len(map_msg_map.data))
        print(len(map_msg_gmap.data))
        if (len(map_msg_gmap.data) !=0 ): 
            for i in range(len(map_msg_map.data)):
                if (map_msg_gmap.data[i] > map_msg_map.data[i]):
                    #print(map_msg_gmap.data[i])
                    #merged_map.data.append(map_msg_gmap.data[i])
                    merged_map.data[i]=map_msg_gmap.data[i]
                else: 
                    #print(map_msg_map.data[i])
                    #merged_map.data.append(map_msg_map.data[i])
                    merged_map.data[i]=map_msg_map.data[i]
            merge_pub.publish(merged_map)
            print("Published")
        
        rate.sleep() # Sleeps for 1/rate sec 