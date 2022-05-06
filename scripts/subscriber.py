#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Range # Message type used in the node

'''
"sub_callback" is the callback method of the subscriber. Argument "msg" contains the received data.
'''
def sub_callback_front(msg):
    rospy.loginfo("Front sensor range: %f", msg.range)

def sub_callback_left(msg):
    rospy.loginfo("Left sensor range: %f", msg.range)

def sub_callback_right(msg):
    rospy.loginfo("Right sensor range: %f", msg.range)

rospy.init_node('subscriber_py') # Init the node with name "subscriber_py"

rospy.Subscriber("sensor/ir_front", Range, sub_callback_front, queue_size=10)
rospy.Subscriber("sensor/ir_left", Range, sub_callback_left, queue_size=10)
rospy.Subscriber("sensor/ir_right", Range, sub_callback_right, queue_size=10) 

rospy.loginfo("subscriber.py node has started and subscribed to sensor/ir_*** topics")

ref_range_min = 0.02
ref_range_max = 0.035

# TODO: log markers if range is smaller than reference value
def publish_curb():
    pass

def publish_edge():
    pass

rospy.spin() 