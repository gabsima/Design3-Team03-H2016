from Client.BaseStation.WorldVision.worldImage import WorldImage
import os
import base64
from Client.BaseStation.WorldVision.worldVision import worldVision
import cv2


if __name__ == '__main__':

    camera = cv2.VideoCapture(0)
    camera.set(3, 720)
    camera.set(4, 720)
    ret, frame = camera.read()
    geometricalImage = WorldImage(frame)
    #worldVision = worldVision()

    while(True):
        ret, frame = camera.read()
        #frame = cv2.imread('Images/Test6.jpg')

        geometricalImage.setMap(frame)
        geometricalImage.addLabels(frame)

        worldImage = geometricalImage.drawMapOnImage(frame)
        cv2.imshow("Monde", worldImage)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # geometricalImage = WorldImage(frame)
        # geometricalImage.setMap()
        # geometricalImage.defineShapesColor()
        # geometricalImage.addLabels()
        # worldImage = geometricalImage.drawMapOnImage()

        # geometricalImage = WorldImage(frame)
        # geometricalImage.setMap()
        # geometricalImage.addLabels()
        # worldImage = geometricalImage.drawMapOnImage()


    #cap.release()
    cv2.destroyAllWindows()

