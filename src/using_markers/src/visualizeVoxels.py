import rospy
import numpy as np
import tf
import math
import geometry_msgs.msg
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker, MarkerArray
import random

class GridVisualization:
    def __init__(self, xs=0.5, ys=0.5, zs=0.5, w = 30, d = 20, h = 10):
        self.xs = xs
        self.ys = ys
        self.zs = zs

        self.w = w
        self.d = d
        self.h = h

        rospy.init_node("VoxelGrid")
        self.rate = rospy.Rate(1)

        self.pub = rospy.Publisher('/voxels', MarkerArray, queue_size=10)

    def sampleVoxels(self):
        return np.random.rand(self.h, self.d, self.w) < 0.5

    def visualizeVoxels(self, grid):
        markerArr = MarkerArray()        
        pts = 0
        # color = np.random.rand(1,3)
        for i in range(self.h):
            for j in range(self.d):
                for k in range(self.w):
                    if grid[i, j, k]>0:
                        pts += 1
                        m = Marker()
                        m.header.frame_id = "/my_frame"
                        m.header.stamp = rospy.Time.now()
                        m.ns = "voxels"
                        m.action = m.ADD
                        m.type = m.CUBE
                        m.id = pts 

                        m.scale.x = self.xs 
                        m.scale.y = self.ys
                        m.scale.z = self.zs

                        m.color.r = 1.0
                        m.color.g = 1.0
                        m.color.a = 1.0

                        m.pose.position.x = self.xs * (k-self.w//2)
                        m.pose.position.y = self.zs * (i-self.h//2)
                        m.pose.position.z = 5-(self.ys * (j-self.d//2))
                        # m.pose.position.x = self.xs * k
                        # m.pose.position.y = self.zs * i
                        # m.pose.position.z = 5-(self.ys * j)

                        markerArr.markers.append(m)

        return markerArr

    def visualizeVoxels1(self, arr):
        markerArr = MarkerArray()        
        pts = 0

        for i in range(len(arr)):
            pts += 1
            m = Marker()
            m.header.frame_id = "/my_frame"
            m.header.stamp = rospy.Time.now()
            m.ns = "voxels"
            m.action = m.ADD
            m.type = m.CUBE
            m.id = pts 

            m.scale.x = self.xs 
            m.scale.y = self.ys
            m.scale.z = self.zs

            m.color.r = 1.0
            m.color.g = 1.0
            m.color.a = 1.0

            m.pose.position.x = arr[i][0]
            m.pose.position.y = arr[i][2]
            m.pose.position.z = arr[i][1]

            markerArr.markers.append(m)

        return markerArr

    def run(self, grid):
        # s = self.sampleVoxels()
        while not rospy.is_shutdown():
            mk = self.visualizeVoxels(grid)
            self.pub.publish(mk)
            self.rate.sleep()

    def run1(self, arr):
        mk = self.visualizeVoxels1(arr)
        while not rospy.is_shutdown():
            self.pub.publish(mk)
            self.rate.sleep()

        


# if __name__== '__main__':
#     print("3D grid being visualized")
#     GridVisualization(xs=0.1, ys=0.1, zs=0.1,w = 60, d = 60, h=10).run()
