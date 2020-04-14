#!/usr/bin/env python
import rospy
import random
from std_msgs.msg import Int32


rospy.init_node('publisher_node')

pub = rospy.Publisher('counter', Int32, queue_size=10)

count = Int32()
count.data = 9

rate = rospy.Rate(10)

while not rospy.is_shutdown():
	count = random.randint(-10,10)
	pub.publish(count)
	rate.sleep()