import numpy as np
import math
import os
import time
from subprocess import call


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

fls = ['NumObj.txt', 'rs_data.txt', 'grasp_obj.txt', 'pos_data.txt', 'Wait.txt', 'grasp.txt']
f = open("Wait.txt", "w")
f.write("%d\t%d\n" % (Wait, end_program))
f.close()
print "start"
rc = call("./c.sh", shell=True)
print "end"
m = 0

# POSITION OF OBJECTS, MAY CHOOSE TO DO ELSEWHERE
xo = [0.5, -0.5, 0.5]  # defined from point cloud
yo = [-0.5, 0.5, 0.5]  # defined from point cloud
zo = [0.2, 0.2, 0.2]  # defined from point cloud


while end_program == 1:
    xo_sign = np.sign(xo)
    yo_sign = np.sign(yo)
    zo_sign = np.sign(zo)

    # THE FOLLOWING IS PSUEDO-CODE, NEEDS YOLO
    Wait = 0
    f = open("Wait.txt", "w")  # open file for overwrite
    f.write("%d\t%d\n" % (Wait, end_program))
    f.close()

    nms = input("Number of Objects?")  # NUMBER OF OBJECTS FROM YOLO DETECTION
    nms = nms-1
    choice = input("Which Object?")         # BOUNDING BOX # FROM USER INPUT
    choice = choice-1

    Wait = 1
    try:

        if choice >= nms:
            choice = nms-1
        elif choice < 0:
            choice = 0
        else:
            choice = 0

    except (type(choice) == str) or (type(choice) == str):
        nms = input("Number of Objects?")  # NUMBER OF OBJECTS FROM YOLO DETECTION
        choice = input("Which Object?")  # BOUNDING BOX # FROM USER INPUT

    f = open("Wait.txt", "w")
    f.write("%d\t%d\n" % (Wait, end_program))
    f.close()
    #print("Define cartesian positions of the objects ... ")

    NumObj = nms  # Number of objects (identified in Yolo)
    Obj = choice   # object wanting to grasp


    # detect the current working directory and print it

    flag = [0, 0, 1]  # 0 = cylinder, 1=rectangular prism
    dim = [[0.02, 0.4], [0.02, 0.4], [0.02, 0.4]] # dimensions of the objects (defined from yolo)
    xp = xo[Obj]
    yp = yo[Obj]
    zp = zo[Obj]

    os.chdir(pth2)
    time.sleep(2.5)

    # overwrite each file and add delay in time for program to respond

    for i in range(len(fls)):
        if i == 0:
            f = open(fls[i], "w")  # open file for overwrite
            f.write("%d" % NumObj)  # NumObj is an integer
            f.close()
        elif i == 1:
            f = open(fls[i], "w")  # open file for overwrite
            for j in range(NumObj+1):
                f.write("%d\t%f\t%f\t%f\t%f\t%f\n" % (flag[j], dim[j][0], dim[j][1], xo[j], yo[j], zo[j]))
            f.close()
        elif i == 2:
            f = open(fls[i], "w")  # open file for overwrite
            f.write("%d\t%f\t%f\t%f\t%f\t%f\n" % (flag[Obj], dim[Obj][0], dim[Obj][1], xo[Obj], yo[Obj], zo[Obj]))
            f.close()
        elif i == 3:
            if dim[Obj][0] < 0.05:  # verify object is graspable
                if dim[Obj][0] > dim[Obj][1]:   # verify that the height is greater than the radius
                    azx = 0.1
                    azy = 0.1
                    azz = 1.5
                else:
                    azx = 0.1
                    azy = 1.5
                    azz = 0.1
            else:
                print("Object is too big to grasp!")
                continue
            f = open(fls[i], "w")  # open file for overwrite
            f.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (xp, yp, zp, azx, azy, azz))
            f.close()
            xo[Obj] = xp         # updates the location of the object to the location of the gripper
            yo[Obj] = yp
            zo[Obj] = zp
            f.close()
        elif i == 4:
            Wait = 0
            f = open(fls[i], "w")  # open file for overwrite
            f.write("%d\t%d\n" % (Wait, end_program))
            f.close()
            #end_program = input("End Program?")
            #if end_program == 1:
            Wait = 1
            g = input("Grasp?")
            if (g == "yes") or (g == "Yes") or (g == "Y") or (g == 0):
                grasp = 0
            elif (g == 1) or (g == "No") or (g == "no") or (g == "N"):
                grasp = 1
            else:
                print("Invalid input! Leaving gripper open")
            f = open(fls[i], "w")
            f.write("%d\t%d\n" % (Wait, end_program))
            f.close()
        elif i == 5:
            f = open(fls[i], "w")  # open file for overwrite
            f.write("%d\t%d" % (grasp, Obj))  # grasp is an integer
            f.close()

