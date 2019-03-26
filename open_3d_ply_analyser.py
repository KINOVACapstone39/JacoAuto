# examples/Python/Tutorial/Basic/pointcloud.py

import numpy as np
import math
import open3d
from open3d import *
import os
import time
fls = ['NumObj.txt', 'grasp.txt', 'rs_data.txt', 'grasp_obj.txt', 'pos_data.txt', 'Wait.txt']

pth1 = os.getcwd()
print(pth1)
pth2 = "/home"
os.chdir(pth2)
pth2 = os.getcwd()
os.chdir(pth1)
key = 0
m = 0
NumPose = 2
ang = [0.1, 1.5, 0.1]
while key == 0:
    m = m+1

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

    #point_cloud = open3d.PointCloud()
    #point_cloud.points = open3d.Vector3dVector(newdata)

    #draw_geometries([pcd])
    #draw_geometries([point_cloud])

    Wait = 0
    end_program = 1
    # POSITION OF OBJECTS, MAY CHOOSE TO DO ELSEWHERE
    xo = [0.25, 0.5, -0.3]  # defined from point cloud
    yo = [0.25, -0.5, 0.3]  # defined from point cloud
    zo = [0, -0.10, -0.10]  # defined from point cloud
    xo_sign = np.sign(xo)
    yo_sign = np.sign(yo)
    zo_sign = np.sign(zo)

    # THE FOLLOWING IS PSUEDO-CODE, NEEDS YOLO
    nms = input("Number of Objects?")  # NUMBER OF OBJECTS FROM YOLO DETECTION
    nms = nms-1
    choice = input("Which Object?")         # BOUNDING BOX # FROM USER INPUT
    choice = choice - 1
    print("Define cartesian positions of the objects ... ")
    NumObj = nms  # Number of objects (identified in Yolo)
    Obj = choice   # object wanting to grasp


    # detect the current working directory and print it

    flag = [0, 0, 1]  # 0 = cylinder, 1=rectangular prism
    dim = [[0.02, 0.4], [0.02, 0.4], [0.02, 0.4]] # dimensions of the objects (defined from yolo)
    if NumPose == 1:
        xp = xo
        yp = yo
        zp = zo
    elif NumPose > 1:
        xp = np.zeros((NumPose, NumObj))
        yp = xp
        zp = xp
    else:
        print("Number of poses must be defined greater than zero!")
        break



    os.chdir(pth2)


    # overwrite each file and add delay in time for program to respond
    for i in range(len(fls)):
        f = open(fls[i], "w")       # open file for overwrite
        if i == 0:
            f.write("%d" % NumObj)  # NumObj is an integer
            f.close()
        elif i == 1:
            f.write("%d\t%d" % (grasp, Obj))  # grasp is an integer
            f.close()
        elif i == 2:
            for j in range(NumObj):
                    f.write("%d\t%f\t%f\t%f\t%f\t%f\n" % (flag[j], dim[j][0], dim[j][1], xo[j], yo[j], zo[j]))
                    if j == Obj:
                        f1 = open(fls[i+1], "w")  # no appending
                        f1.write("%f\t%f\t%f\t%f\t%f\n" % (dim[j][0], dim[j][1], xo[j], yo[j], zo[j]))
                        f1.close()
                    f.close()
        elif i == 4:
            if dim[Obj][0] < 0.05:
                if dim[Obj][0] > dim[Obj][1]:
                    ang = [0.3, 0.3, 1.5]
                elif dim[Obj][0] < dim[Obj][1]:
                    ang = [0.1, 1.5, 0.1]
                else:
                    ang = [0.0, 0.0, 1.5]
            else:
                print("Object is too big to grasp!")

            for j in range(NumPose):
                f = open(fls[i], "w")
                if j == 0:
                    xp[j] = 0.5
                    xp[j] = 0.5
                    yp[j] = 0.5
                if (j > 0) and (j < NumPose):
                    xp[j] = (xo[Obj] - xp[0])*j / NumPose  # x pose, up to three poses defined for 1 grasp
                    yp[j] = (yo[Obj] - yo[0])*j / NumPose  # y pose
                    zp[j] = (zo[Obj] - zo[0])*j / NumPose  # z pose
                    f.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (xp[j], yp[j], zp[j], ang[0], ang[1], ang[2]))
                elif j == NumPose:
                    grasp = int(1)  # 0 = close, 1 = open
                    xp[j] = (xo[Obj] - xp[0]) * j / NumPose  # x pose, up to three poses defined for 1 grasp
                    yp[j] = (yo[Obj] - yo[0]) * j / NumPose  # y pose
                    zp[j] = (zo[Obj] - zo[0]) * j / NumPose  # z pose
                    xp[j] = xp[j] - xo_sign[Obj]*0.02
                    yp[j] = yp[j] - yo_sign[Obj]*0.02
                    zp[j] = zp[j] - zo_sign[Obj]*0.02
                    f.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (xp[j], yp[j], zp[j], ang[0], ang[1], ang[2]))
                    f.close()
                    grasp = int(0)          # will perform the grasp operation next loop
                    xo[Obj] = xp[j]         # updates the location of the object to the location of the gripper
                    yo[Obj] = yp[j]
                    zo[Obj] = zp[j]
                f.close()
                sleep_time = 10 / NumPose
                time.sleep(sleep_time)
        elif i == 5:
            f.write("%d\t%d\n" % (Wait, end_program))
            f.close()
            Wait = input("Continue?")
            end_program = input("End Program?")
            f = open(fls[i], "w")
            f.write("%d\t%d\n" % (Wait, end_program))
            f.close()
    os.chdir(pth1)












