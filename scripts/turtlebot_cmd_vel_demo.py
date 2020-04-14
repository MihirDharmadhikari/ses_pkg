#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10)

def vel_publisher(lin_vel, ang_vel):
	vel_cmd = Twist()
	vel_cmd.linear.x = lin_vel
	vel_cmd.angular.z = ang_vel

	vel_pub.publish(vel_cmd)

def shutdown_func():
	vel_publisher(0.0, 0.0)	

if __name__ == '__main__':
	rospy.init_node('turtlebot_vel_pub', anonymous=True)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		vel_publisher(0.2, 0.1)
		rate.sleep()
		rospy.on_shutdown(shutdown_func)
