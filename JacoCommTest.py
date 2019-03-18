import numpy as np
import math
import os
import time
NumPose = 2
pth1 = os.getcwd()
print(pth1)
pth2 = "/home/acis"
os.chdir(pth2)
pth2 = os.getcwd()
print(pth2)

Wait = 0
grasp = 1
end_program = 1

fls = ['NumObj.txt', 'grasp.txt', 'rs_data.txt', 'grasp_obj.txt', 'pos_data.txt', 'Wait.txt']
ang = [0.0, 0.0, 0.0]
f = open("Wait.txt", "w")
f.write("%d\t%d\n" % (Wait, end_program))
f.close()

m = 0

while end_program == 1:
    m = m + 1
    if m == 1:
        # POSITION OF OBJECTS, MAY CHOOSE TO DO ELSEWHERE
        xo = [0.5, -0.5, 0.5]  # defined from point cloud
        yo = [-0.5, 0.5, 0.5]  # defined from point cloud
        zo = [0.5, 0.5, 0.5]  # defined from point cloud
        xo_sign = np.sign(xo)
        yo_sign = np.sign(yo)
        zo_sign = np.sign(zo)

    # THE FOLLOWING IS PSUEDO-CODE, NEEDS YOLO
    nms = input("Number of Objects?")  # NUMBER OF OBJECTS FROM YOLO DETECTION
    nms = nms
    choice = input("Which Object?")         # BOUNDING BOX # FROM USER INPUT
    choice = choice
    #print("Define cartesian positions of the objects ... ")
    NumObj = nms  # Number of objects (identified in Yolo)
    Obj = choice   # object wanting to grasp


    # detect the current working directory and print it

    flag = [0, 0, 1]  # 0 = cylinder, 1=rectangular prism
    dim = [[0.02, 0.4], [0.02, 0.4], [0.02, 0.4]] # dimensions of the objects (defined from yolo)
    xp = xo
    yp = yo
    zp = zo
    xp[Obj] = xo[Obj] - xo_sign[Obj] * 0.02
    yp[Obj] = yo[Obj] - yo_sign[Obj] * 0.02
    zp[Obj] = zo[Obj] - zo_sign[Obj] * 0.02

    os.chdir(pth2)


    # overwrite each file and add delay in time for program to respond
    for i in range(len(fls)):
        if i == 0:
            f = open(fls[i], "w")  # open file for overwrite
            f.write("%d" % NumObj)  # NumObj is an integer
            f.close()
        elif i == 1:
            f = open(fls[i], "w")  # open file for overwrite
            f.write("%d\t%d" % (grasp, Obj))  # grasp is an integer
            f.close()
        elif i == 2:
            f = open(fls[i], "w")  # open file for overwrite
            for j in range(NumObj):
                if m > 1:
                    if j != Obj:
                        f.write("%d\t%f\t%f\t%f\t%f\t%f\n" % (flag[j], dim[j][0], dim[j][1], xo[j], yo[j], zo[j]))
                elif m == 1:
                    f.write("%d\t%f\t%f\t%f\t%f\t%f\n" % (flag[j], dim[j][0], dim[j][1], xo[j], yo[j], zo[j]))

            f.close()
        elif i == 3:
            f = open(fls[i], "w")  # open file for overwrite
            f.write("%d\t%f\t%f\t%f\t%f\t%f\n" % (flag[Obj], dim[Obj][0], dim[Obj][1], xo[Obj], yo[Obj], zo[Obj]))
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
                continue
            f = open(fls[i], "w")  # open file for overwrite
            f.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (xp[Obj], yp[Obj], zp[Obj], ang[0], ang[1], ang[2]))
            f.close()
            xo[Obj] = xp[Obj]         # updates the location of the object to the location of the gripper
            yo[Obj] = yp[Obj]
            zo[Obj] = zp[Obj]
            f.close()
        elif i == 5:
            Wait = 0
            f = open(fls[i], "w")  # open file for overwrite
            f.write("%d\t%d\n" % (Wait, end_program))
            f.close()
            end_program = input("End Program?")
            if end_program == 1:
                Wait = 1
                f = open(fls[i], "w")
                f.write("%d\t%d\n" % (Wait, end_program))
                f.close()
            g = input("Grasp?")
            if (g == "yes") or (g == "Yes") or (g == "Y") or (g == 0):
                grasp = 0
            elif (g == 1) or (g == "No") or (g == "no") or (g == "N"):
                grasp = 1
            else:
                print("Invalid input! Leaving gripper open")

