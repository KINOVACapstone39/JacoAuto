import cv2 as cv2
import numpy as np

# Write down conf, nms thresholds,inp width/height
confThreshold = 0.25
nmsThreshold = 0.1
inpWidth = 608  # 320,426,608
inpHeight = 608  # 320,426,608

# Load names of classes and turn that into a list
classesFile = "coco.names"
classes = None

with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Model configuration
modelConf = 'yolov3.cfg'
modelWeights = 'yolov3.weights'


def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIDs = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:

            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > confThreshold:
                centerX = int(detection[0] * frameWidth)
                centerY = int(detection[1] * frameHeight)

                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)

                left = int(centerX - width / 2)
                top = int(centerY - height / 2)

                classIDs.append(classID)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]

        drawPred(classIDs[i], confidences[i], left, top, left + width, top + height)


def drawPred(classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv2.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # A fancier display of the label from learnopencv2.com
    # Display the label at the top of the bounding box
    # labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    # top = max(top, labelSize[1])
    # cv2.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
    # (255, 255, 255), cv2.FILLED)
    # cv2.rectangle(frame, (left,top),(right,bottom), (255,255,255), 1 )
    # cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)
    cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)


def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()

    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Set up the net

net = cv2.dnn.readNetFromDarknet(modelConf, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Process inputs
winName = 'DL OD with Opencv2'
cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
cv2.resizeWindow(winName, 1000, 1000)

image = 'color_img.jpg'

cap = cv2.VideoCapture(1)

while cv2.waitKey(1) < 0:
    # get frame from video
    hasFrame, frame = cap.read()

    # Create a 4D blob from a frame

    blob = cv2.dnn.blobFromImage(frame, 0.003921, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)

    # Set the input the the net
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))

    postprocess(frame, outs)

    # show the image
    cv2.imshow(winName, frame)
    cv2.waitKey(5000)

















