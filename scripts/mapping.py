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

lidar_range = 100
front_range = 0
left_range = 0
right_range = 0

# initialize node
rospy.init_node('range_to_occupancy_grid_node')

# listener of transforms between the base_link and the world frame
robot_pose = tf.TransformListener()

# Initialize occupancy grid message
map_msg = OccupancyGrid()
map_msg.header.frame_id = 'map'
resolution = 0.01
width = 500
height = 500

# Initialize car pose relative to world
x_robot = 0.0
y_robot = 0.0

# square size of the robot footprint [m]
footprint = 0.15

# Map update rate (defaulted to 5 Hz)
rate = 5.0

# Range data
car_range = 0.0

def set_free_cells(grid, position, size):
    # set free the cells occupied by the car
    # grid:				ndarray [width,height]
    # position:			[x y] pose of the car
    # size: 			r     radius of the footprint
    global resolution

    off_x = position[1] // resolution + width  // 2
    off_y = position[0] // resolution + height // 2

    # set the roi to 1: known free positions
    for i in range(-size//2, size//2):
    	for j in range(-size//2, size//2):
    		grid[int(i + off_x), int(j + off_y)] = 1

def set_free_cells2(grid, size):
    # set the occupied cells when detecting an obstacle
    # grid:				ndarray [width,height]
    # position:			[x y] pose of the car
    # orientation:      quaternion, orientation of the car
    global resolution

    if (right_range < 0.04):
        position, quaternion = robot_pose.lookupTransform("/odom", "/base_ir_right", rospy.Time(0))
        off_x = position[1] // resolution + width  // 2
        off_y = position[0] // resolution + height // 2

        for i in range(-size//2, size//2):
            for j in range(-size//2, size//2):
                grid[int(i + off_x), int(j + off_y)] = 1

    if (left_range < 0.04):
        position, quaternion = robot_pose.lookupTransform("/odom", "/base_ir_left", rospy.Time(0))
        off_x = position[1] // resolution + width  // 2
        off_y = position[0] // resolution + height // 2

        for i in range(-size//2, size//2):
            for j in range(-size//2, size//2):
                grid[int(i + off_x), int(j + off_y)] = 1

    if (front_range < 0.04):
        position, quaternion = robot_pose.lookupTransform("/odom", "/base_ir_front", rospy.Time(0))
        off_x = position[1] // resolution + width  // 2
        off_y = position[0] // resolution + height // 2

        for i in range(-size//2, size//2):
            for j in range(-size//2, size//2):
                grid[int(i + off_x), int(j + off_y)] = 1

def set_obstacle(grid, size):
    # set the occupied cells when detecting an obstacle
    # grid:				ndarray [width,height]
    # position:			[x y] pose of the car
    # orientation:      quaternion, orientation of the car
    global resolution

    if (right_range > 0.04):
        position, quaternion = robot_pose.lookupTransform("/odom", "/base_ir_right", rospy.Time(0))
        off_x = position[1] // resolution + width  // 2
        off_y = position[0] // resolution + height // 2

        for i in range(-size//2, size//2):
            for j in range(-size//2, size//2):
                grid[int(i + off_x), int(j + off_y)] = 100

    if (left_range > 0.04):
        position, quaternion = robot_pose.lookupTransform("/odom", "/base_ir_left", rospy.Time(0))
        off_x = position[1] // resolution + width  // 2
        off_y = position[0] // resolution + height // 2

        for i in range(-size//2, size//2):
            for j in range(-size//2, size//2):
                grid[int(i + off_x), int(j + off_y)] = 100

    if (front_range > 0.04):
        position, quaternion = robot_pose.lookupTransform("/odom", "/base_ir_front", rospy.Time(0))
        off_x = position[1] // resolution + width  // 2
        off_y = position[0] // resolution + height // 2

        for i in range(-size//2, size//2):
            for j in range(-size//2, size//2):
                grid[int(i + off_x), int(j + off_y)] = 100

    '''
    #t = robot_pose.getLatestCommonTime("/base_footprint", "/map")
    position, quaternion = robot_pose.lookupTransform("/odom", "/base_link", rospy.Time(0))
    position_front, quaternion_front = robot_pose.lookupTransform("/odom", "/base_ir_front", rospy.Time(0))
    position_left, quaternion_left = robot_pose.lookupTransform("/odom", "/base_ir_left", rospy.Time(0))
    position_right, quaternion_right = robot_pose.lookupTransform("/odom", "/base_ir_right", rospy.Time(0))


    off_x = position[1] // resolution + width  // 2
    off_y = position[0] // resolution + height // 2

    #euler = tf.transformations.euler_from_quaternion(orientation)

    if (right_range > 0.04 or left_range > 0.04 or front_range > 0.04):


        for i in range(-size//2, size//2):
            for j in range(-size//2, size//2):
                grid[int(i + off_x), int(j + off_y)] = 100
        #obstacle = [position[1], position[0]]

        #rospy.loginfo("FOUND OBSTACLE AT: x:%f y:%f", obstacle[0], obstacle[1])
    '''
    '''
        # set probability of occupancy to 100 and neighbour cells to 50
        grid[int(obstacle[0]), int(obstacle[1])] = int(100)
        if  grid[int(obstacle[0]+1), int(obstacle[1])]   < int(1):
            grid[int(obstacle[0]+1), int(obstacle[1])]   = int(50)
        if  grid[int(obstacle[0]), 	 int(obstacle[1]+1)] < int(1):
            grid[int(obstacle[0]),   int(obstacle[1]+1)] = int(50)
        if  grid[int(obstacle[0]-1), int(obstacle[1])]   < int(1):
            grid[int(obstacle[0]-1), int(obstacle[1])]   = int(50)
        if  grid[int(obstacle[0]),   int(obstacle[1]-1)] < int(1):
            grid[int(obstacle[0]),   int(obstacle[1]-1)] = int(50)
    '''
'''
"sub_callback" is the callback method of the subscriber. Argument "msg" contains the received data.
'''
def sub_callback_front(msg):
    #rospy.loginfo("Front sensor range: %f", msg.range)
    global front_range
    front_range = msg.range

def sub_callback_left(msg):
    #rospy.loginfo("Left sensor range: %f", msg.range)
    global left_range
    left_range = msg.range

def sub_callback_right(msg):
    #rospy.loginfo("Right sensor range: %f", msg.range)
    global right_range
    right_range = msg.range

# rospy.init_node('subscriber_py') # Init the node with name "subscriber_py"

rospy.Subscriber("sensor/ir_front", Range, sub_callback_front, queue_size=10)
rospy.Subscriber("sensor/ir_left", Range, sub_callback_left, queue_size=10)
rospy.Subscriber("sensor/ir_right", Range, sub_callback_right, queue_size=10) 

# Publishers
occ_pub = rospy.Publisher("/robot/map", OccupancyGrid, queue_size = 10)

rospy.loginfo("subscriber.py node has started and subscribed to sensor/ir_*** topics")

ref_range_min = 0.02
ref_range_max = 0.035

# TODO: log markers if range is smaller than reference value
def publish_curb():
    pass

def publish_edge():
    pass

# rospy.spin()

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
    print("teszt")

    while not rospy.is_shutdown():
        
        position = (0,0,0)
        
        try:
            #t = robot_pose.getLatestCommonTime("/base_footprint", "/map")
            position, quaternion = robot_pose.lookupTransform("/odom", "/base_link", rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        '''
        try:
            t = robot_pose.getLatestCommonTime("/base_link", "/sonar_link")
            #position_sonar, quaternion_sonar = robot_pose.lookupTransform("/base_link", "/sonar_link", t)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        '''
		# write 0 (null obstacle probability) to the free areas in grid
        #set_free_cells(grid, position, int(footprint//resolution))
        #set_free_cells2(grid, int(0.1//resolution))

		# write p>0 (non-null obstacle probability) to the occupied areas in grid
        set_obstacle(grid, int(0.1//resolution))

		# stamp current ros time to the message
        map_msg.header.stamp = rospy.Time.now()

		# build ros map message and publish
        for i in range(width*height):
            map_msg.data[i] = grid.flat[i]
        occ_pub.publish(map_msg)
        print("Published")

        loop_rate.sleep() 