# The following program writes data to the files according to the programming of pick_place.cpp
# please adhere file writing to these methods
import os.path
import cv2
import numpy as np
n = 0
while n<1000:   # this is an arbitrary number of way-points, it would be ideally as long as the user wants to use the arm
    # this data is arbitrarily chosen. You would need to define it elsewhere within this loop
    NumObj = int(3)  # Number of objects
    Obj = int(1)    # object wanting to grasp
    grasp = int(0)  # integer 0 or 1 (bool)
    flag = [0, 0, 1]
    dim = [[0.02, 0.4], [0.02, 0.4], [0.02, 0.4]]
    x = [0.5, 0.5, 0.5]
    xp = [0.5, 0.5, 0.5]
    y = [0.5, 0.5, 0.5]
    yp = [0.5, 0.5, 0.5]
    z = [0.5, 0.5, 0.5]
    zp = [0.5, 0.5, 0.5]
    ang = [0.1, 1.5, 0.1]
    #detect the current working directory and print it
    pth1 = os.getcwd()
    print(pth1)
    fls = ['NumObj.txt', 'grasp.txt', 'rs_data.txt', 'grasp_obj.txt', 'pos_data.txt']
    for i in range(len(fls)):
        f = open(fls[i], "w")    # no appending
        if i == 0:
            f.write("%d" % NumObj)  # NumObj is an integer
        elif i == 1:
            f.write("%d\t%d" % (grasp, Obj))  # grasp is an integer
        elif i == 2:
            for j in range(NumObj):
                    f.write("%d\t%f\t%f\t%f\t%f\t%f\n" % (flag[j], dim[j][0], dim[j][1], x[j], y[j], z[j]))
                    if j == Obj:
                        f1 = open(fls[i+1], "w")  # no appending
                        f1.write("%f\t%f\t%f\t%f\t%f\n" % (dim[j][0], dim[j][1], xp[j], yp[j], zp[j]))
                        xp[j] = x[j]
                        yp[j] = y[j]
                        zp[j] = z[j]
        elif i == 4:
            f = open(fls[i],"w")
            f.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (x[0],x[1],x[2], ang[0], ang[1], ang[2]))
    n = n+1