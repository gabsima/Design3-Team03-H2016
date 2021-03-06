from Client.BaseStation.WorldVision.worldImage import WorldImage
import os
import base64
from Client.BaseStation.WorldVision.worldVision import worldVision
import cv2

def printPosition(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        resultFile = open(resultFileName, 'a')
        resultFile.write("("+str(x)+","+str(y)+")")
        resultFile.close()

beginingPhoto = 181
endPhoto = 213

for i in range(beginingPhoto,endPhoto+1):
    pictureNumber = i
    resultFileName = 'Results/Picture ' + str(pictureNumber) + '.txt'
    frameFileName = 'Frames/Picture ' + str(pictureNumber) + '.jpg'
    resultFile = open(resultFileName, 'w')
    resultFile.write("CenterOfMass:")
    resultFile.close()
    frame = cv2.imread(frameFileName)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',printPosition)
    cv2.imshow('image',frame)
    cv2.waitKey(0)


