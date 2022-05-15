#!/usr/bin/env python3

import rospy
import numpy
import tf
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import Range 

lidar_range = 100
front_range = 0
left_range = 0
right_range = 0

# initialize node
rospy.init_node('range_to_occupancy_grid_node')

# listener of transforms between the base_link and the odom frame
robot_pose = tf.TransformListener()

# Initialize occupancy grid message
map_msg = OccupancyGrid()
map_msg.header.frame_id = 'map'
resolution = 0.01
width = 500
height = 500

# Initialize pose
x_robot = 0.0
y_robot = 0.0

# reference ranges for sensors
ref_range_min = 0.02
ref_range_max = 0.035


# Map update rate (defaulted to 5 Hz)
rate = 5.0

def set_free_cells(grid, size):
    # set free cells under the robot 
    global resolution

    # get base_link position
    position, quaternion = robot_pose.lookupTransform("/odom", "/base_link", rospy.Time(0))
    off_x = position[1] // resolution + width  // 2
    off_y = position[0] // resolution + height // 2

    for i in range(-size//2, size//2):
            for j in range(-size//2, size//2):
                grid[int(i + off_x), int(j + off_y)] = 1

    
def set_obstacle(grid, size):
    # set the occupied cells when detecting edges
    global resolution

    if (right_range > ref_range_max):
        # get right sensor position
        position, quaternion = robot_pose.lookupTransform("/odom", "/base_ir_right", rospy.Time(0))
        off_x = position[1] // resolution + width  // 2
        off_y = position[0] // resolution + height // 2

        for i in range(-size//2, size//2):
            for j in range(-size//2, size//2):
                grid[int(i + off_x), int(j + off_y)] = 100

    if (left_range > ref_range_max):
        # get left sensor position
        position, quaternion = robot_pose.lookupTransform("/odom", "/base_ir_left", rospy.Time(0))
        off_x = position[1] // resolution + width  // 2
        off_y = position[0] // resolution + height // 2

        for i in range(-size//2, size//2):
            for j in range(-size//2, size//2):
                grid[int(i + off_x), int(j + off_y)] = 100

    if (front_range > ref_range_max):
        # get front sensor position
        position, quaternion = robot_pose.lookupTransform("/odom", "/base_ir_front", rospy.Time(0))
        off_x = position[1] // resolution + width  // 2
        off_y = position[0] // resolution + height // 2

        for i in range(-size//2, size//2):
            for j in range(-size//2, size//2):
                grid[int(i + off_x), int(j + off_y)] = 100


# callback functions to range data
def sub_callback_front(msg):
    global front_range
    front_range = msg.range

def sub_callback_left(msg):
    global left_range
    left_range = msg.range

def sub_callback_right(msg):
    global right_range
    right_range = msg.range

# subscribers
rospy.Subscriber("sensor/ir_front", Range, sub_callback_front, queue_size=10)
rospy.Subscriber("sensor/ir_left", Range, sub_callback_left, queue_size=10)
rospy.Subscriber("sensor/ir_right", Range, sub_callback_right, queue_size=10) 

# publisher
occ_pub = rospy.Publisher("/robot/map", OccupancyGrid, queue_size = 10)

rospy.loginfo("mapping.py node has started")

# main function
if __name__ == '__main__':

    # set grid parameters
    if rospy.has_param("occupancy_rate"):
        rate = rospy.get_param("occupancy_rate")

    if rospy.has_param("grid_resolution"):
        resolution = rospy.get_param("grid_resolution")

    if rospy.has_param("grid_width"):
        width = rospy.get_param("grid_width")

    if rospy.has_param("grid_height"):
        height = rospy.get_param("grid_height")

	# fill map_msg with the parameters from launchfile
    map_msg.info.resolution = resolution
    map_msg.info.width = width
    map_msg.info.height = height
    map_msg.data = list(range(width*height))

	# initialize grid with -1 (unknown)
    grid = numpy.ndarray((width, height), buffer=numpy.zeros((width, height), dtype=numpy.int),
	         dtype=numpy.int)
    grid.fill(int(-1))

	# set map origin [meters]
    map_msg.info.origin.position.x = - width // 2 * resolution
    map_msg.info.origin.position.y = - height // 2 * resolution

    loop_rate = rospy.Rate(rate)

    while not rospy.is_shutdown():
        
        position = (0,0,0)
        
        # get position
        try:
            position, quaternion = robot_pose.lookupTransform("/odom", "/base_link", rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        #set free cells on map
        set_free_cells(grid, int(0.18//resolution))

		# set edges on map
        set_obstacle(grid, int(0.15//resolution))

		# stamp current ros time to the message
        map_msg.header.stamp = rospy.Time.now()

		# build ros occupancy grid message and publish
        for i in range(width*height):
            map_msg.data[i] = grid.flat[i]
        occ_pub.publish(map_msg)

        loop_rate.sleep() 