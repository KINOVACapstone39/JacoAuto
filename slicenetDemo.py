# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 00:01:27 2019

@author: David
"""
import numpy as np
from open3d import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

pcd = read_point_cloud("1.ply")
matrix = np.asarray(pcd.points)
draw_geometries([pcd])

planes = 5

ZLimits = np.array((np.amin(matrix[:, 2]), np.amax(matrix[:, 2])))
planeResolution = abs(ZLimits[0] - ZLimits[1])/(planes-1)
z = np.linspace(ZLimits[0], ZLimits[1], planes)

for i in range(len(matrix[:, 0])):
    currentPtz = matrix[i, 2]
    d = np.zeros(planes)
    for j in range(planes):
        d[j] = abs(currentPtz - z[j])
    dmin = min(d)
    I = d.argmin()
    matrix[i, 2] = z[I]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(matrix[:,0], matrix[:,1], matrix[:,2], zdir='z', s=5, c=None, depthshade=True)
