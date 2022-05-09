#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Range 

lidar_range = 100
front_range = 0
left_range = 0
right_range = 0

def sub_callback_lidar(msg):
    #rospy.loginfo("New message.")
    #print(msg.ranges[360])
    # print(len(msg.ranges))
    global lidar_range
    lidar_range = msg.ranges[360]

def sub_callback_front(msg):
    rospy.loginfo("Front sensor range: %f", msg.range)
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
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    rospy.Subscriber("/scan", LaserScan, sub_callback_lidar, queue_size=10)
    rospy.Subscriber("sensor/ir_front", Range, sub_callback_front, queue_size=10)
    rospy.Subscriber("sensor/ir_left", Range, sub_callback_left, queue_size=10)
    rospy.Subscriber("sensor/ir_right", Range, sub_callback_right, queue_size=10)

    #Receiveing the user's input
    print("Let's move your robot")
    speed = 1
    distance = 100
    isForward = 1

    #Checking if the movement is forward or backwards
    if(isForward):
        vel_msg.linear.x = abs(int(speed))
        vel_msg.angular.z = 0
    else:
        vel_msg.angular.z = abs(int(speed))
        vel_msg.linear.x = 0
    #Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    

    while not rospy.is_shutdown():

        if (right_range > 0.04 or left_range > 0.04 or front_range > 0.04 or lidar_range < 0.4):
            i=0
            vel_msg.angular.z = abs(int(speed))
            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            while(i<10):
                velocity_publisher.publish(vel_msg)
                i=i+1

        else:
            vel_msg.linear.x = 0.05
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0

            velocity_publisher.publish(vel_msg)

            print(front_range)


        #Setting the current time for distance calculus
        # 0 = rospy.Time.now().to_sec()
        # current_distance = 0

        #Loop to move the turtle in an specified distance
        #while(current_distance < int(distance)):
            #Publish the velocity
            #velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
            #t1=rospy.Time.now().to_sec()
            #Calculates distancePoseStamped
            #current_distance= int(speed)*(t1-t0)
        #After the loop, stops the robot
        #vel_msg.linear.x = 0
        #Force the robot to stop
        #velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass
