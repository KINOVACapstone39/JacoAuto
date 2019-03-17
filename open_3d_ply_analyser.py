# examples/Python/Tutorial/Basic/pointcloud.py

import numpy as np
import math
from open3d import *

if __name__ == "__main__":

    print("Load a ply point cloud, print it, and render it")
    pcd = read_point_cloud("1.ply")
    data = np.asarray(pcd.points)
    size = data.shape[0]
    thetaX = math.pi * 20 / 180
    array1 = np.array([1.0, 0.0, 0.0])
    array2 = np.array([0, math.cos(thetaX), -1 * math.sin(thetaX)])
    array3 = np.array([0, math.sin(thetaX), math.cos(thetaX)])

    for x in range(size):
        currentData = data[x]
        currentData.transpose()
        transformation = np.array([array1, array2, array3])
        currentData = np.matmul(currentData, transformation)
        currentData.transpose()
        data[x] = currentData
    colors = np.asarray(pcd.colors)
    size = colors.shape[0]
    count = 0
    reducedData = []
    color = np.array([0.00392156862745098, 0.00392156862745098, 0.00392156862745098])
    for x in range(size):
        if color in colors[x]:
            reducedData.append(data[x])
    newdata = np.asarray(reducedData)

    planes = 5

    ZLimits = np.array((np.amin(newdata[:, 2]), np.amax(newdata[:, 2])))
    planeResolution = abs(ZLimits[0] - ZLimits[1]) / (planes - 1)
    z = np.linspace(ZLimits[0], ZLimits[1], planes)

    for i in range(len(newdata[:, 0])):
        currentPtz = newdata[i, 2]
        d = np.zeros(planes)
        for j in range(planes):
            d[j] = abs(currentPtz - z[j])
        dmin = min(d)
        I = d.argmin()
        newdata[i, 2] = z[I]

    point_cloud = open3d.PointCloud()
    point_cloud.points = open3d.Vector3dVector(newdata)

    draw_geometries([pcd])
    draw_geometries([point_cloud])
