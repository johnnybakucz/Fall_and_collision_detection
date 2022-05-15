#!/usr/bin/env python3
<<<<<<< HEAD
import rospy
import tf
from nav_msgs.msg import OccupancyGrid
=======
from turtle import position
import rospy
import numpy
import math
import tf
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Pose
>>>>>>> main
from sensor_msgs.msg import Range # Message type used in the node

# initialize node
rospy.init_node('merge_maps')

robot_pose = tf.TransformListener()

rate = rospy.Rate(10) # 1 Hz

<<<<<<< HEAD
# init occupancy grid
map_msg_map = OccupancyGrid()
map_msg_gmap = OccupancyGrid()
merged_map = OccupancyGrid()
merged_map.header.frame_id = 'map'
=======
map_msg_map = OccupancyGrid()
map_msg_gmap = OccupancyGrid()
merged_map = OccupancyGrid()
merged_map.header.frame_id = 'merged_map'
>>>>>>> main
resolution = 0.025
width = 800
height = 800

<<<<<<< HEAD
# callbacks to get map datas
def sub_callback_gmapping(msg):
=======
def sub_callback_gmapping(msg):
    #rospy.loginfo("Front sensor range: %f", msg.range)
>>>>>>> main
    global map_msg_gmap
    map_msg_gmap = msg

def sub_callback_mapping(msg):
<<<<<<< HEAD
    global map_msg_map
    map_msg_map = msg

# subscriber
rospy.Subscriber("robot/map", OccupancyGrid, sub_callback_mapping, queue_size=10)
rospy.Subscriber("map", OccupancyGrid, sub_callback_gmapping, queue_size=10)

# publisher
merge_pub = rospy.Publisher("/merged/map", OccupancyGrid, queue_size = 10)

rospy.loginfo("mege_maps.py started")
=======
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
>>>>>>> main

# main function
if __name__ == '__main__':

<<<<<<< HEAD
=======
    # fill map_msg with the parameters from launchfile
    merged_map.info.resolution = resolution
    merged_map.info.width = width
    merged_map.info.height = height
    merged_map.data = list(range(width*height))

    merged_map.info.origin.position.x = - width // 2 * resolution
    merged_map.info.origin.position.y = - height // 2 * resolution

    '''
>>>>>>> main
    # set grid parameters
    if rospy.has_param("occupancy_rate"):
        rate = rospy.get_param("occupancy_rate")

    if rospy.has_param("grid_resolution"):
        resolution = rospy.get_param("grid_resolution")

    if rospy.has_param("grid_width"):
        width = rospy.get_param("grid_width")

    if rospy.has_param("grid_height"):
        height = rospy.get_param("grid_height")
<<<<<<< HEAD

    # fill map_msg with the parameters from launchfile
    merged_map.info.resolution = resolution
    merged_map.info.width = width
    merged_map.info.height = height
    merged_map.data = list(range(width*height))

    merged_map.info.origin.position.x = - width // 2 * resolution
    merged_map.info.origin.position.y = - height // 2 * resolution

=======
    '''
>>>>>>> main
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