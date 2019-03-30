import os
pth1 = os.getcwd()
length = 1000
for i in range(length):
    print(pth1)
    pth2 = "/home"
    os.chdir(pth2)
    pth2 = os.getcwd()
    print(pth2)
    os.chdir(pth1)
    #pth1 = os.getcwd()
    #print(pth2)