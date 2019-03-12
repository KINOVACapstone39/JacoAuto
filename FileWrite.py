#import the os module
import os.path
import cv2
import numpy as np

# detect the current working directory and print it
pth1 = os.getcwd()
print ("The current working directory is %s" % pth1)
pth2 = "/home/acis/catkin_ws/src/kinova-ros/kinova_moveit/kinova_arm_moveit_demo/src"
print ("The current working directory is %s" % pth2)
fl = "CartData"

cmp_f = os.path.join(pth2, fl+".txt")
f1 = open(cmp_f, "w+")

for i in range(10):
   # f1.write("This is line %d\r\n" % (i+1))


# repoed http://answers.opencv.org/question/208331/getting-3d-points-from-pointcloud-to-show-objects-positions/



f1.close()