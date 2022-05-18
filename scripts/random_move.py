#!/usr/bin/env python3
import rospy
import random
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Range 

#init ranges
lidar_range = 100
front_range = 0
left_range = 0
right_range = 0

# reference ranges for sensors
ref_range_min = 0.02
ref_range_max = 0.035


# callbacks for lidar and range data
def sub_callback_lidar(msg):
    global lidar_range
    lidar_range = msg.ranges[310:410]
    lidar_range = min(lidar_range)

def sub_callback_front(msg):
    global front_range
    front_range = msg.range

def sub_callback_left(msg):
    global left_range
    left_range = msg.range

def sub_callback_right(msg):
    global right_range
    right_range = msg.range

# moving
def move():
    # init a new node
    rospy.init_node('random_move', anonymous=True)
    rate = rospy.Rate(10) # 1 Hz
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    # subscribers
    rospy.Subscriber("/scan", LaserScan, sub_callback_lidar, queue_size=10)
    rospy.Subscriber("sensor/ir_front", Range, sub_callback_front, queue_size=10)
    rospy.Subscriber("sensor/ir_left", Range, sub_callback_left, queue_size=10)
    rospy.Subscriber("sensor/ir_right", Range, sub_callback_right, queue_size=10)


    while not rospy.is_shutdown():

        # if near to obstacle or edge, turn for random time
        if (right_range > ref_range_max or left_range > ref_range_max or front_range > ref_range_max or lidar_range < 0.3):
            
            i=0

            if (right_range > ref_range_max): 
                vel_msg.angular.z = -1
            else: 
                vel_msg.angular.z = 1

            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            x = random.randint(20,35)

            while(i<x):
                velocity_publisher.publish(vel_msg)
                i=i+1 
                rate.sleep() # Sleeps for 1/rate sec

        # if no obstacles go forward
        else:
            vel_msg.linear.x = 0.07  # speed
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0

            velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException: pass
