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
obj = 1
# Object location
b = 0.05
h = 0.2
xo = 0.13
yo = -0.41
zo = -0.02
azx = 0.1
azy = 1.5
azz = 0.1
xs = np.sign(xo)
ys = np.sign(yo)
zs = np.sign(zo)
# Home Position
xh = 0.25
yh = -0.30
zh = 0.5
#azx = 0.1
#azy = 1.5
#azz = 0.1

fls = ['comnd.txt', 'obj.txt', 'pos.txt']
f = open("Wait.txt", "w")
f.write("%d\t%d\t%d\n" % (Wait, end_program, grasp))
f.close()


while end_program == 1:
    for i in range(2):
        # RUN PROGRAM TO SELECT OBJECT HERE
        if i == 0:
            ''' b = input("b:")
            h = input("h:")
            xo = input("x:")
            xs = np.sign(xo)
            yo = input("y:")
            ys = np.sign(yo)
            zo = input("z:")
            zs = np.sign(zo)
            azx = input("axx:")
            azy = input("azy:")
            azz = input("azz:") 
            grasp = 1 '''

            f = open("obj.txt", "w")
            #if grasp == 0:
            #    xo = xpp
            #    yo = ypp
            #    zo = zpp
            f.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (b, h, xo, yo, zo, azx, azy, azz))
            f.close()
            f = open("pos.txt","w")
            if grasp == 1:
                xp = xo - xs*0.015
                yp = yo - ys*0.015
                zp = zo
                f.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (xp, yp, zp, azx, azy, azz))
            elif grasp == 0:
                f.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (xh, yh, zh, azx, azy, azz))
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
        elif i == 1:
            grasp = input("grasp?")
            Wait = 1
            f = open("comnd.txt", "w")  # open file for overwrite
            f.write("%d\t%d\t%d\n" % (Wait, end_program, grasp))
            f.close()
            cont = input("Continue?")
        #f = open("comnd.txt", "w")  # open file for overwrite
        #    f.write("%d\t%d\t%d\n" % (Wait, end_program, grasp))
        #    f.close()

