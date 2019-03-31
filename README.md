# JacoAuto for OS Ubuntu 16.04
WARNING: THIS SOFTWARE IS NOT TESTED, UNEXPECTED MOTION OF THE ARM MAY RESULT. 
FOR RESEARCH PURPOSES ONLY. STAY CLEAR BY 1 METRE, AND KEEP ALL LARGE OR DISRUPTIVE OBJECTS CLEAR BY 1 METRE.

Python code for implementing autonomous control of the Jaco Assistive Robot for grasping and returning an object from a
specific location, and returning it to the home position. All commits made frequently prior  to April 6th.
JacoAuto is a dependent source code repository that allows grasping of objects from a select location for
the purspose of fullfilling the requirements of an undergraduate CAPSTONE design project. This method is used by the University of British Columbia (UBC) Okanagan Advanced Control and Intelligent Systems (ACIS) laboratory for research purposes. It not designated as a product of sale or a final distributable software. Elements of it are intellectual property of Kinova Robotics, and other source distributors. We disclaim all liability for any software errors that occur and result in damages to property or the health and well-being of the user. USE AT YOUR OWN RISK. The implementation relies on third party dependencies, namely the following:

Prerequisite software package installation:

YOLOV3 Darknet

MoveIt! RViz

Gazebo

GraspIt!

Jennifer Buehler dependencies

Jennifer Buehler tutorials

Intel RealSense SDK and python libraries

OpenCV version 4.0.1 (may not work for  earlier versions)

Python 2.7. (discontinued as of January 2020, use Intel Python 3.5 libraries if available after this date)

Prerequisite actions:
1. The simple environment of the JACO robot must be changed in src/.../pick_place.cpp, otherwise it conforms to the environment
   used by the ACIS laboratory.


Path directories for files:
1. catkin_ws must fall under the home directory.
2. All python files must be accessible to a python project in PyCharm or your preferred python IDE.
3. Read-Write TXT files and c.sh must fall under the home directory, otherwise their directory must be changed in open_3d_ply_analyser.py. 

Executing the program:
1. Open the Python project. With correctly calibrated position of robot and camera, run rs_viewer.py.
2. While rs_viewer.py is running, open gnome-terminal. Type "sudo -s" or whichever command allows you to act as root user.
3. Type "bash c.sh"

Using the program:
1. Clicking on a window outside the execution terminal, type "s"
2. Clicking in the terminal, select the object to grasp as a number (e.g. 1,2,3). Hit "Enter".
3. Delete any windows that open with filtered point clouds in them.
4. Press "1" and "Enter" for JACO to move towards the object with an open gripper.
5. Press "0" and "Enter" for the gripper to close and return to a psuedo-home position.
6. Press "1" in a point cloud window to stop execution, otherwise press "s" to select a new object.

These programs are for demonstration purposes only. They do not allow the manipulation of objects, and do not provide an intuitive user interface.
These may be developed hopefully with the method's growth by the ACIS laboratory, third party users, or Kinova Robotics.
