# examples/Python/Tutorial/Basic/pointcloud.py

import numpy as np
import math
import statistics as st
import os
import time
import cv2 as cv2

# Home Position

# Camera calibration
xh = 0.00
yh = -0.40
zh = 0.5
azx = 0.001
azy = 1.501
azz = 0.001
azxh = -1.501
azzh = azz

# Global variables
Wait = 0
grasp = 1
end_program = 1
obj = 1
grasp = 1
NumPose = 2

# home path
pth1 = os.getcwd()
print(pth1)
pth2 = "/home/acis"

os.chdir(pth2)
pth2 = os.getcwd()
print(pth2)

# Robot communication files
fls = ['comnd.txt', 'obj.txt', 'pos.txt']
f = open("Wait.txt", "w")

# Write to files
f.write("%d\t%d\t%d\n" % (Wait, end_program, grasp))
f.close()

os.chdir(pth1)

if __name__ == "__main__":
    # Point angles transformation to robot coordinates
    print("Load a ply point cloud, print it, and render it")
    pcd = read_point_cloud("1.ply")
    data = np.asarray(pcd.points)
    size = data.shape[0]
    thetaX = math.pi * -1 / 180
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
    color = np.array([255, 0, 255])
    for x in range(size):
        if color in colors[x]:
            reducedData.append(data[x])
    newdata = np.asarray(reducedData)

    graspData = []

    # Slicing and filtering points
    planes = int(round((np.amax(newdata[:, 2]) - np.amin(newdata[:, 2])) / 0.2))

    ZLimits = np.array((np.amin(newdata[:, 2]), np.amax(newdata[:, 2])))
    planeResolution = abs(ZLimits[0] - ZLimits[1]) / (planes - 1)
    z = np.linspace(ZLimits[0], ZLimits[1], planes)

    for i in range(len(newdata[:, 2])):
        currentPtz = newdata[i, 2]
        d = np.zeros(planes)
        for j in range(planes):
            d[j] = abs(currentPtz - z[j])
        dmin = min(d)
        tests = d.argmin()
        if d.argmin() == planes - 1:
            graspData.append(newdata[i])
        I = d.argmin()

    # Slicing object vertically
    planes = 5
    convertedGraspData = np.asarray(graspData)
    newdata2 = convertedGraspData
    ZLimits = np.array((np.amin(newdata2[:, 1]), np.amax(newdata2[:, 1])))
    planeResolution = abs(ZLimits[0] - ZLimits[1]) / (planes - 1)
    z = np.linspace(ZLimits[0], ZLimits[1], planes)

    for i in range(len(newdata2[:, 1])):
        currentPtz = newdata2[i, 1]
        d = np.zeros(planes)
        for j in range(planes):
            d[j] = abs(currentPtz - z[j])
        dmin = min(d)
        tests = d.argmin()
        if d.argmin() == planes - 1:
            graspData.append(newdata[i])
        I = d.argmin()
        newdata2[i, 1] = z[I]

    points = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0],
             [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]]
    lines = [[0, 1], [0, 2], [1, 3], [2, 3],
            [4, 5], [4, 6], [5, 7], [6, 7],
            [0, 4], [1, 5], [2, 6], [3, 7]]
    colors = [[1, 0, 0] for i in range(len(lines))]
    line_set = LineSet()
    line_set.points = Vector3dVector(points)
    line_set.lines = Vector2iVector(lines)
    line_set.colors = Vector3dVector(colors)

    point_cloud = open3d.PointCloud()
    point_cloud.points = open3d.Vector3dVector(newdata)

    grasp_cloud = open3d.PointCloud()
    grasp_cloud.points = open3d.Vector3dVector(convertedGraspData)
    np.savetxt("foo2.csv", convertedGraspData, delimiter=",")

    slice_cloud = open3d.PointCloud()
    slice_cloud.points = open3d.Vector3dVector(newdata2)

    ''' draw_geometries([line_set, grasp_cloud])
    draw_geometries([line_set, point_cloud])
    draw_geometries([pcd])
    draw_geometries([line_set, slice_cloud])'''

    #vis = Visualizer()
    #vis.destroy_window()
    #vis.create_window(window_name='Post YOLO Point Cloud', width=400, height=400, left=1000, right=30)
    #vis.add_geometry(point_cloud)

    #vis.update_geometry()
    #vis.poll_events()
    #vis.update_renderer()

    vis2 = Visualizer()
    vis2.destroy_window()
    vis2.create_window(window_name='SliceNet Point Cloud', width=540, height=540, left=1000, right=0)
    vis2.add_geometry(slice_cloud)

    vis2.update_geometry()
    vis2.poll_events()
    vis2.update_renderer()


    # vis3 = Visualizer()
    # vis3.create_window(width=400, height=400, left=1000, right=800)
    # vis3.add_geometry(grasp_cloud)
    #
    # vis3.update_geometry()
    # vis3.poll_events()
    # vis3.update_renderer()



    # coordinate transforms
    xTrans = -0.615
    yTrans = -0.47
    zTrans = -0.04
    size = convertedGraspData.shape[0]

    for x in range(size):
        tempY = convertedGraspData[x][0] - yTrans
        tempZ = convertedGraspData[x][1] - zTrans
        tempX = convertedGraspData[x][2] - xTrans
        convertedGraspData[x] = [-tempX, -tempY, -tempZ]

    # Object dimensions
    b = np.amax(convertedGraspData[:, 1]) - np.amin(convertedGraspData[:, 1])
    h = np.amax(convertedGraspData[:, 2]) - np.amin(convertedGraspData[:, 2])

    # Object locations
    xo = np.around(np.amin(convertedGraspData[:, 0]) + b / 2, decimals=3)
    print(xo)
    yo = np.around(st.mean(convertedGraspData[:, 1]), decimals=3)
    print(yo)
    zo = np.around(h/2.0+zTrans, decimals=3)
    print(zo)
    xs = np.sign(xo)
    ys = np.sign(yo)
    zs = np.sign(zo)
    os.chdir(pth2)
    b = 0.05
    h = 0.35
    # xo = 0.13
    # yo = -0.43
    zo = h/2.0-0.102
    print(pth2)
    for i in range(NumPose):
        # RUN PROGRAM TO SELECT OBJECT HERE
        # grasp = input("grasp?")
        key = 3
        while key != 1:
            key = cv2.waitKey(1)
            if key == ord("o"):
                grasp = 1
                break
            elif key == ord("g"):
                grasp = 0
                break

        # Open txt file of object
        f = open("obj.txt", "w")
        f.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (b, h, float(xo), float(yo), float(zo), azx, azy, azz))
        f.close()
        f = open("pos.txt", "w")
        if grasp == 1:
            xp = float(xo) - float(xs * 0.02)
            yp = float(yo) - float(ys * 0.02)
            zp = -0.05
            f.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (xp, yp, zp, azx, azy, azz))
        elif grasp == 0:
            f.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (xh, yh, zh, azxh, azy, azzh))
        f.close()
        # THE FOLLOWING IS PSUEDO-CODE, NEEDS YOLO
        Wait = 1
        f = open("comnd.txt", "w")  # open file for overwrite
        f.write("%d\t%d\t%d\n" % (Wait, end_program, grasp))
        f.close()
        time.sleep(2.5)
        Wait = 0
        f = open("comnd.txt", "w")  # open file for overwrite
        f.write("%d\t%d\t%d\n" % (Wait, end_program, grasp))
        f.close()
        time.sleep(2.5)


       #f = open("comnd.txt", "w")  # open file for overwrite
       #    f.write("%d\t%d\t%d\n" % (Wait, end_program, grasp))
       #    f.close()

    os.chdir(pth1)
    print("Press the 's' key for selection mode ...")
    '''draw_geometries([point_cloud])'''