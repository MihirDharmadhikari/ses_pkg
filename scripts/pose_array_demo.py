#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseArray, Pose


rospy.init_node('publisher_node')

pub = rospy.Publisher('pose_array', PoseArray, queue_size=10)

pa = PoseArray()

pa.header.frame_id = "map"

for i in range(5):
	p = Pose()
	p.position.x = i
	p.position.y = 0
	p.position.z = 0
	p.orientation.x = 0
	p.orientation.y = 0
	p.orientation.z = 0
	p.orientation.w = 1

	pa.poses.append(p)

rate = rospy.Rate(10)

while not rospy.is_shutdown():
	pub.publish(pa)
	rate.sleep()