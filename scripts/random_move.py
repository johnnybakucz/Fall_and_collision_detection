#!/usr/bin/env python3
import rospy
import random
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Range 

lidar_range = 100
front_range = 0
left_range = 0
right_range = 0

def sub_callback_lidar(msg):
    global lidar_range
    lidar_range = msg.ranges[330:390]
    lidar_range = min(lidar_range)
    #print(lidar_range)

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

def move():
    # Starts a new node
    rospy.init_node('random_move', anonymous=True)
    rate = rospy.Rate(10) # 1 Hz
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    rospy.Subscriber("/scan", LaserScan, sub_callback_lidar, queue_size=10)
    rospy.Subscriber("sensor/ir_front", Range, sub_callback_front, queue_size=10)
    rospy.Subscriber("sensor/ir_left", Range, sub_callback_left, queue_size=10)
    rospy.Subscriber("sensor/ir_right", Range, sub_callback_right, queue_size=10)


    while not rospy.is_shutdown():
        if (right_range > 0.04 or left_range > 0.04 or front_range > 0.04 or lidar_range < 0.4):
            i=0
            if (right_range > 0.04): 
                vel_msg.angular.z = -1
            else: 
                vel_msg.angular.z = 1
            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            x = random.randint(20,35)
            #print(x)
            while(i<x):
                velocity_publisher.publish(vel_msg)
                i=i+1
                #print("forgas")   
                rate.sleep() # Sleeps for 1/rate sec


        else:
            vel_msg.linear.x = 0.07
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0

            velocity_publisher.publish(vel_msg)
            #print("Elore")
            #rate.sleep() # Sleeps for 1/rate sec



if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass
