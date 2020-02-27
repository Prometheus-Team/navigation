import numpy as np
import math
from scipy import ndimage
from visualizeVoxels import GridVisualization
import tf.transformations as tra 

import pickle
import time
'''
Note
- Each voxel represents 0.5m and if decompostion is required
we will use octree creating 8 voxels from each voxel with 0.25m
size each

'''
width = 640
height = 480

class Location:
    x = y = z = heading = 0
    def __init__(self, x, y, z, heading):
        self.setLocation(x, y, z, heading)

    def setLocation(self, x, y, z, heading):
        self.x = x
        self.y = y
        self.z = z
        self.heading = heading

class Mapper:
    def __init__(self, x, y, z, size):
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.initMap()

    def initMap(self):
        self.mapVal = np.zeros((self.z, self.y, self.x))
        self.mapRep = np.zeros((self.z, self.y, self.x))

        self.mapRep[self.z//2, self.y//2, self.x//2] = 5

    def modifyMap(self, location, map):
        pass

    def minimizeMapSize(self, map, stride, iteration):
        pass

    def getMap(self, location, size=0):
        pass

    def worldCoords(self, width, height):
        hfov_degrees, vfov_degrees = 57, 43
        hFov = math.radians(hfov_degrees)
        vFov = math.radians(vfov_degrees)
        cx, cy = width/2, height/2
        fx = width/(2*math.tan(hFov/2))
        fy = height/(2*math.tan(vFov/2))
        xx, yy = np.tile(range(width), height), np.repeat(range(height), width)
        xx = (xx-cx)/fx
        yy = (yy-cy)/fy
        return xx, yy

    def posFromDepth(self, depth, xx, yy):
        length = depth.shape[0] * depth.shape[1]
        print(depth.shape)

        # depth[self.edges(depth) > 0.3] = 1e6  # Hide depth edges       
        z = depth.reshape(length)

        return np.dstack((xx*z, yy*z, z)).reshape((length, 3))
    
    def loadImg(self, fName):
        # img = np.genfromtxt(fName+'.csv', delimiter=',')
        # np.save(fName+".npy", img)

        img = np.load(fName+".npy")
        return img

    # Compute edge magnitudes
    def edges(self, d):
        dx = ndimage.sobel(d, 0)  # horizontal derivative
        dy = ndimage.sobel(d, 1)  # vertical derivative
        return np.abs(dx) + np.abs(dy)
    
    # droneLoc - current drone location 
    def transform(self, droneLoc, points, axis=(0, 0, 1)):
        rotAngle = droneLoc.heading

        translationVec = (droneLoc.x, droneLoc.y, droneLoc.z)
        traMat = tra.rotation_matrix(rotAngle, axis).dot(tra.translation_matrix(translationVec))
        y = np.ones((len(points), 4))
        y[:,:-1] = points
        z = traMat.dot(y.transpose()).transpose()

        return np.round(z[:,:-1], 3)

    def getCurLoc(self):
        return Location(0,0,0, 0)

    def test(self):
        r = GridVisualization(xs=self.size, ys=self.size, zs=self.size,w = self.x, d = self.y, h=self.z)
        tInit = time.time()
        w = width//2
        h = height//2

        fNames = ['test7', 'test1']

        locs = [(0,0,0,0),(0,0,0,0)]
        for i in range(0,1):
            depth = self.loadImg('../TestImgs/' + fNames[i])
            
            xx, yy = self.worldCoords(int(w), int(h))
            
            res = self.posFromDepth(depth, xx, yy)

            loc = Location(locs[i][0],locs[i][1],locs[i][2],locs[i][3])
            # loc = self.getCurLoc()
            # loc.heading = headings[i]
            
            traRes = self.transform(loc, res, (0,1,0))
            traRes = traRes/self.size
            # print(traRes)

            # floor negative nos and ceiling positive nos
            absTraRes = abs(traRes)
            b = np.divide(traRes, absTraRes, out=np.zeros_like(traRes), where=absTraRes!=0)
            traRes = (traRes + b).astype(int)

            self.changeMap(traRes)

        print(time.time()-tInit)
        r.run(self.mapRep)

    def changeMap(self, depth):
        depth[:, 0:3] += [50,50,50]
        mapReps = np.zeros((self.z, self.y, self.x))
        mapReps[depth[:, 2], depth[:, 1], depth[:, 0]] += 1

        # if more than 2 point is projected to the voxel its considered occupied so its changed in the main map array
        self.mapRep += mapReps > 0


mapperInst = Mapper(100,100,100,0.25)
mapperInst.test()