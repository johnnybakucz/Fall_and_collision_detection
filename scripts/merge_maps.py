#!/usr/bin/env python3
import rospy
import tf
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import Range # Message type used in the node

# initialize node
rospy.init_node('merge_maps')

robot_pose = tf.TransformListener()

rate = rospy.Rate(10) # 1 Hz

# init occupancy
map_msg_map = OccupancyGrid()
map_msg_gmap = OccupancyGrid()
merged_map = OccupancyGrid()
merged_map.header.frame_id = 'map'
resolution = 0.025
width = 800
height = 800

# callbacks to get map datas
def sub_callback_gmapping(msg):
    global map_msg_gmap
    map_msg_gmap = msg

def sub_callback_mapping(msg):
    global map_msg_map
    map_msg_map = msg

# subscriber
rospy.Subscriber("robot/map", OccupancyGrid, sub_callback_mapping, queue_size=10)
rospy.Subscriber("map", OccupancyGrid, sub_callback_gmapping, queue_size=10)

# publisher
merge_pub = rospy.Publisher("/merged/map", OccupancyGrid, queue_size = 10)

rospy.loginfo("mege_maps.py started")

# main function
if __name__ == '__main__':

    # fill map_msg with the parameters from launchfile
    merged_map.info.resolution = resolution
    merged_map.info.width = width
    merged_map.info.height = height
    merged_map.data = list(range(width*height))

    merged_map.info.origin.position.x = - width // 2 * resolution
    merged_map.info.origin.position.y = - height // 2 * resolution

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