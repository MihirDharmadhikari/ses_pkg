#!/usr/bin/env python
import rospy
import numpy
import math
import tf
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class Traveller(object):
	def __init__(self):
		# Variables
		self.odom = Odometry()
		self.curr_pos = numpy.array((0.0,0.0))
		self.goal = numpy.array((0.0,0.0))
		self.yaw = 0.0

		# For the controller:
		self.threshold = 0.1  # Tolerance from goal
		self.ang_threshold = 0.25  # zero lin vel angle

		self.max_lin_vel = 0.22
		self.max_ang_vel = 1.0
		self.min_lin_vel = 0.1
		self.min_ang_vel = 0.0

		self.k_lin = 1.0  # Proportional gain for lin vel
		self.k_ang = 0.3  # Proportional gain for ang vel

		# Publisher
		self.vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
		# Subscriber
		rospy.Subscriber('odom', Odometry, self.odom_cb)

	def odom_cb(self, odom):
		self.odom = odom
		self.curr_pos[0] = odom.pose.pose.position.x
		self.curr_pos[1] = odom.pose.pose.position.y
		robot_orientation = tf.transformations.euler_from_quaternion([odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w])
		self.yaw = robot_orientation[2]

	def vel_publisher(self, lin_vel, ang_vel):
		vel_cmd = Twist()
		vel_cmd.linear.x = lin_vel
		vel_cmd.angular.z = ang_vel

		self.vel_pub.publish(vel_cmd)

	def goto(self, goal):
		lin_error = 0.0
		ang_error = 0.0

		lin_vel = 0.0
		ang_vel = 0.0

		# compute lin error
		lin_error = numpy.linalg.norm(goal - self.curr_pos)
		# compute ang error
		theta = math.atan2((goal[1]-self.curr_pos[1]), (goal[0]-self.curr_pos[0]))
		ang_error = theta - self.yaw;

		while lin_error > self.threshold:
			# compute lin error
			lin_error = numpy.linalg.norm(goal - self.curr_pos)
			# compute ang error
			theta = math.atan2((goal[1]-self.curr_pos[1]), (goal[0]-self.curr_pos[0]))
			ang_error = theta - self.yaw;
			print "errors:", lin_error, ang_error
			if abs(ang_error) > self.ang_threshold:
				lin_vel = 0.0
			else:
				lin_vel = max(self.min_lin_vel, min(self.k_lin*lin_error, self.max_lin_vel))

			ang_vel = min(self.k_ang*ang_error, self.max_ang_vel)
			print "Vels:  ", lin_vel, ang_vel

			self.vel_publisher(lin_vel, ang_vel)

		self.vel_publisher(0.0, 0.0)
		print "TARGET REACHED"

	def shutdown_func(self):
		self.vel_publisher(0.0, 0.0)	



if __name__ == '__main__':
	rospy.init_node('turtlebot_goto_node', anonymous=True)
	rate = rospy.Rate(10)

	traveller = Traveller()

	gx = float(input("Enter goal x: "))
	gy = float(input("Enter goal y: "))
	traveller.goto(numpy.array((gx, gy)))
	
	rospy.spin()
	rospy.on_shutdown(traveller.shutdown_func)
