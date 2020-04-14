#!/usr/bin/env python

import rospy
from basic.srv import PoseSrv, PoseSrvResponse, PoseSrvRequest

def pose_vis_client(x, y, z):
    # Is the service available?
    rospy.wait_for_service('pose_vis_srv')
    # Safety for the service call
    try:
        # This is the service handler
        pose_vis = rospy.ServiceProxy('pose_vis_srv', PoseSrv)
        # Create request object. This will be passed at the time of service call
        srv_pose_obj = PoseSrvRequest()
        srv_pose_obj.header.frame_id = "map"
        srv_pose_obj.pose.position.x = x
        srv_pose_obj.pose.position.y = y
        srv_pose_obj.pose.position.z = z
        srv_pose_obj.pose.orientation.x = 0.0
        srv_pose_obj.pose.orientation.y = 0.0
        srv_pose_obj.pose.orientation.z = 0.0
        srv_pose_obj.pose.orientation.w = 1.0
        # Call the sesrvice
        resp1 = pose_vis(srv_pose_obj)
        # return the required part of response of the service
        return resp1.success
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


if __name__ == "__main__":
    rospy.init_node('client', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        resp = pose_vis_client(1,1,1)
        rate.sleep()
        print(resp)