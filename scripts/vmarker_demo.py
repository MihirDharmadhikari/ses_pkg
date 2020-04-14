#!/usr/bin/env python

import rospy
from visualization_msgs.msg import Marker

def talker():
	# Initiate node
	rospy.init_node('talker', anonymous=True)
	# Publisher 
	mpub = rospy.Publisher('marker', Marker, queue_size=10)
	# Rate
	rate = rospy.Rate(10)

	# Define the marker
	marker = Marker()
	marker.header.frame_id = "map"
	marker.header.stamp = rospy.Time()
	marker.ns = "my_namespace"
	marker.id = 0
	marker.type = Marker.SPHERE
	marker.action = Marker.ADD
	marker.pose.position.x = 1
	marker.pose.position.y = 1
	marker.pose.position.z = 1
	marker.pose.orientation.x = 0.0
	marker.pose.orientation.y = 0.0
	marker.pose.orientation.z = 0.0
	marker.pose.orientation.w = 1.0
	marker.scale.x = 1
	marker.scale.y = 1
	marker.scale.z = 1
	marker.color.a = 1.0
	marker.color.r = 0.0
	marker.color.g = 1.0
	marker.color.b = 0.0
	
	# Publish
	while not rospy.is_shutdown():
		mpub.publish(marker)
		rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
