from Client.BaseStation.WorldVision.worldImage import WorldImage
import os
import base64
from Client.BaseStation.WorldVision.worldVision import worldVision
import numpy as np
import cv2


if __name__ == '__main__':

    # pictureSources = ['Photos/3105/table 5/Jour/rideau ferme/Picture 1.jpg',
    #                   'Photos/3105/table 5/Jour/rideau ferme/Picture 2.jpg',
    #                   'Photos/3105/table 5/Jour/rideau ferme/Picture 3.jpg',
    #                   'Photos/3105/table 5/Jour/rideau ouvert/Picture 22.jpg',
    #                   'Photos/3105/table 5/Jour/rideau ouvert/Picture 23.jpg',
    #                     'Photos/3105/table 5/Jour/rideau ouvert/Picture 24.jpg',
    #                     'Photos/3105/table 6/Jour/rideau ferme/Picture 18.jpg',
    #                     'Photos/3105/table 6/Jour/rideau ferme/Picture 19.jpg',
    #                     'Photos/3105/table 6/Jour/rideau ferme/Picture 20.jpg',
    #                     'Photos/3105/table 6/Jour/rideau ouvert/Picture 20.jpg',
    #                     'Photos/3105/table 6/Jour/rideau ouvert/Picture 21.jpg',
    #                     'Photos/3105/table 6/Jour/rideau ouvert/Picture 22.jpg',
    #                     'Photos/3109/Table1/Jour/rideau ferme/Picture 12.jpg',
    #                     'Photos/3109/Table1/Jour/rideau ferme/Picture 13.jpg',
    #                     'Photos/3109/Table1/Jour/rideau ferme/Picture 14.jpg',
    #                     'Photos/3109/Table1/Jour/rideau ouvert/Picture 10.jpg',
    #                     'Photos/3109/Table1/Jour/rideau ouvert/Picture 11.jpg',
    #                     'Photos/3109/Table1/Jour/rideau ouvert/Picture 12.jpg',
    #                     'Photos/3109/table 2/Jour/rideau ferme/Picture 14.jpg',
    #                     'Photos/3109/table 2/Jour/rideau ferme/Picture 15.jpg',
    #                     'Photos/3109/table 2/Jour/rideau ferme/Picture 16.jpg',
    #                     'Photos/3109/table 2/Jour/rideau ouvert/Picture 8.jpg',
    #                     'Photos/3109/table 2/Jour/rideau ouvert/Picture 9.jpg',
    #                     'Photos/3109/table 2/Jour/rideau ouvert/Picture 10.jpg',
    #                     'Photos/3109/table3/Jour/rideau ferme/Picture 16.jpg',
    #                     'Photos/3109/table3/Jour/rideau ferme/Picture 17.jpg',
    #                     'Photos/3109/table3/Jour/rideau ferme/Picture 18.jpg',
    #                     'Photos/3109/table3/Jour/rideau ouvert/Picture 4.jpg',
    #                     'Photos/3109/table3/Jour/rideau ouvert/Picture 5.jpg',
    #                     'Photos/3109/table3/Jour/rideau ouvert/Picture 6.jpg',
    #                     'Photos/3109/table3/Jour/rideau ouvert/Picture 7.jpg']
    camera = cv2.VideoCapture(0)
    camera.set(3, 3264)
    camera.set(4, 2448)
    #frame = cv2.imread('Photos/3105/table 5/jour/rideau ouvert/Picture 22.jpg')
    #frame = cv2.imread('Images/Test6.jpg')
    #geometricalImage = WorldImage(frame)
    #worldVision = worldVision()

    phoposToVerified = []
    for x in range(198, 213):
        frame = cv2.imread('Photo-Test/Frames/Picture ' + str(x) + '.jpg')

        # x1, x2, y1, y2 = 941, 900 , 711, 659
        # # line equation y = f(X)
        # def line_eq(X):
        #     m = (y2 - y1) / (x2 - x1)
        #     return m * (X - x1) + y1
        #
        # line = np.vectorize(line_eq)
        #
        # x = np.arange(0, 1200)
        # y = line(x).astype(np.uint)
        #
        # cv2.line(frame, (x[0], y[0]), (x[-1], y[-1]), (0,0,0))
        # cv2.imshow("foo",frame)
        # cv2.waitKey()



    while(True):
        ret, frame = camera.read()
        #frame = cv2.imread('Photos/3105/table 5/Jour/rideau ferme/Picture 1.jpg')
        cv2.resize(frame, (960,720))
        geometricalImage = WorldImage()
        geometricalImage.buildMap(frame)
        geometricalImage.updateRobotPosition(frame)
        geometricalImage.addLabels(frame)
        # worldV = worldVision()
        # map = worldV.getCurrentImage()
        worldImage = geometricalImage.drawMapOnFrame(frame)
        #print(geometricalImage.getMap().robot.findCenterOfMass())

        cv2.imshow('Picture ' + str(x), worldImage)


        # geometricalImage = WorldImage(frame)
        # geometricalImage.setMap()
        # geometricalImage.addLabels()
        # worldImage = geometricalImage.drawMapOnImage()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #cap.release()


