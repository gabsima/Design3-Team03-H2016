from worldImage import WorldImage
import os
import base64
import cv2

class worldVision:

    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, 3264)
        self.camera.set(4, 2448)
        ret, frame = self.camera.read()
        frame = cv2.resize(frame, (960, 720))
        self.mapImage = WorldImage(frame)
        self.mapImage.buildMap(frame)
        self.mapImage.addLabels(frame)


    def getCurrentImage(self):
        ret, frame = self.camera.read()
        frame = cv2.resize(frame, (960, 720))
        self.mapImage.updateRobotPosition(frame)
        worldImage = self.mapImage.drawMapOnImage(frame)

        return worldImage

    def getCurrentMap(self):
        ret, frame = self.camera.read()
        frame = cv2.resize(frame, (960, 720))
        self.mapImage.updateRobotPosition(frame)
        return self.mapImage.getMap()

    def setTarget(self, target):
        self.mapImage.setTarget(target)

