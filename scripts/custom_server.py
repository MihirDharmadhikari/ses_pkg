#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from basic.srv import PoseSrv, PoseSrvResponse, PoseSrvRequest

pub = rospy.Publisher('pose_vis', PoseStamped, queue_size=10)

def handle_pose_vis(req):
    
    p = PoseStamped()  # object to publish
    # Set the object attributes
    p.header = req.header
    p.pose = req.pose
    pub.publish(p)

    # setup response
    res = PoseSrvResponse()
    res.success = True
    return res


def pose_vis_server():
    rospy.init_node('vis_pose')
    s = rospy.Service('pose_vis_srv', PoseSrv, handle_pose_vis)
    rospy.spin()

if __name__ == "__main__":
    pose_vis_server()
