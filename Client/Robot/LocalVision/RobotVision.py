import math
from math import sqrt, cos, sin, radians

import cv2
import numpy as np

from Client.Robot.Movement.WheelManager import WheelManager
from Client.Robot.Mechanical.CameraTower import CameraTower
from Client.BaseStation.WorldVision.colorContainer import ColorContainer


class RobotVision:
    mask = 0

    balayageHori = 0
    LARGEUR_TRESOR_METRE = 2.5
    FOCAL = 508
    largeurTresorPixel = 0

    def __init__(self, wheelManager, cameraTower, videoCapture):
        self.video = videoCapture


        self.robot = wheelManager
        self.camera = cameraTower
        self.camera.step = 0.5
        self.tresor = None
        yellowDown = [0, 90, 90]
        yellowUp = [45, 255, 255]

        greenDown = [0, 100, 0]
        greenUp = [66, 255, 66]

        self.yellowColor = [(yellowDown, yellowUp)]
        self.greenColor = [(greenDown, greenUp)]

    def detectTreasureColor(self):
        self.mask = 0
        for(lower, upper) in self.yellowColor:
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype="uint8")

            self.mask = self.mask + cv2.inRange(self.image, lower, upper)

    def detectChargingStationColor(self):
        self.mask = 0

        colorContainer = ColorContainer()
        hsvImage = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)

        lower = colorContainer.green.lower
        upper = colorContainer.green.higher

        self.mask = self.mask + cv2.inRange(hsvImage, lower, upper)

    def findContour(self):

        (cnts, _) = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        dots = []
        if len(cnts):

            cntsMax = cnts[0]
            for c in cnts:
                if cv2.contourArea(c) > cv2.contourArea(cntsMax):
                    cntsMax = c

            if cv2.contourArea(cntsMax) > 100:
                self.tresor = cntsMax
                x,y,w,h = cv2.boundingRect(self.tresor)
                dots.append((x,y,w,h))
                # if max(w, h) > 100 and max(w, h) < 200:

                cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2)
                self.addLabels(self.tresor)

                self.largeurTresorPixel = max(w,h)
                return self.largeurTresorPixel
            else:
                self.tresor = None
            return 0



    def addLabelsLines(self, dots):
        if len(dots) > 1:
            dotx1 = int(dots[0][2]/2) + dots[0][0]
            dotx2 = int(dots[1][2]/2) + dots[1][0]
            doty1 = int(dots[0][3]/2) + dots[0][1]
            doty2 = int(dots[1][3]/2) + dots[1][1]
            dot1 = (dotx1, doty1)
            dot2 = (dotx2, doty2)

            dots = (dot1, dot2)

            cv2.line(self.image, dots[0], dots[1], (255, 0, 0), 2)
            distance = int(sqrt((dots[0][0] - dots[1][0])**2 + (dots[0][1] - dots[1][1])**2))
            xlabel = int(abs(dots[0][0] - dots[1][0])/2) + min(dots[0][0], dots[1][0])
            ylabel = int(abs(dots[0][1] - dots[1][1])/2) + min(dots[0][1], dots[1][1])
            labelDot = (xlabel, ylabel)

            cv2.putText(self.image, str(distance), labelDot, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1, 8)
            return distance

    def addLabels(self, contour):
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.4
        thickness = 1

        x,y,width,height = cv2.boundingRect(contour)
        point = (x, y - 5)
        cv2.putText(self.image, "Position " + str(x) + " " + str(y) + " " + str(max(width, height)) + " pixel, " + str(cv2.contourArea(contour)) + " area", point, font, scale, (0, 0, 255), thickness, 8)


    def moveCamera(self):
        centerX = False
        centerY = False
        if self.tresor != None:

            x,y,width,height = cv2.boundingRect(self.tresor)
            x = x + width / 2
            y = y + height /2
            ih, iw, ic = self.image.shape
            # print x, y, iw, ih
            squareW = 5
            squareH = 20

            xob = (iw/2-5) - squareW/2 + 15
            yob = ih/2 - squareH/2
            # print xob, yob
            # print xob + square, yob +square

            cv2.rectangle(self.image,(xob, yob),(xob + squareW, yob + squareH),(0,0,255),2)
            cv2.circle(self.image, (x, y), 2, (0,0,255))

            # cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2)

            if x < (xob):
                self.camera.moveCameraLeft()
            elif x > (xob + squareW):
                self.camera.moveCameraRight()
            else:
                centerX = True
            if y < (yob):
                self.camera.moveCameraUp()
            elif y > (yob + squareH):
                self.camera.moveCameraDown()
            else:
                centerY = True

        return centerX and centerY

    def swipeCamera(self):
        if self.tresor == None:
            if self.balayageHori == 0 and self.camera.horizontalDegree < 160:
                self.camera.moveCameraRight()
            else:
                self.balayageHori = 1

            if self.balayageHori == 1 and self.camera.horizontalDegree > 55:
                self.camera.moveCameraLeft()
            else:
                self.balayageHori = 0

        else:
            return True
        return False


    def adjacentDistance(self):
            if self.largeurTresorPixel <= 0:
                return 0
            return self.FOCAL * self.LARGEUR_TRESOR_METRE / self.largeurTresorPixel

    def dista150nceFromCamera(self):
        distanceY = self.adjacentDistance() * cos(radians(123 - self.camera.horizontalDegree) + math.pi / 2)
        distanceX = self.adjacentDistance() * sin(radians(self.camera.verticalDegree - 64))
        # print 123 - self.camera.horizontalDegree, self.camera.verticalDegree, self.distanceAdjascente()

        return (distanceX, distanceY)

    def differenceParraleleLinesTresor(self):
        ret,thresh1 = cv2.threshold(self.image,75,255,cv2.THRESH_BINARY)


        ih, iw, ic = self.image.shape
        col1 = 0
        col2 = iw - 1
        dot1 = []
        dot2 = []


        for i in range(0, ih):
            if np.equal(thresh1[i, 0], np.array([255,255,255])).all():
                dot1 = (0, i)
                break
            if dot1 == []:
                dot1 = (0, ih-1)

        for i in range(0, ih):
            if not np.equal(thresh1[i, col2], np.array([0,0,0])).all():
                dot2 = (col2, i)
                break
            if dot2 == []:
                for i in range(iw - 1, -1, -1):
                    if not np.equal(thresh1[ih - 1, i], np.array([0,0,0])).all():
                        dot2 = (col2, i)
                        break

        # print dot1
        # print dot2
        # dot1 = (1279, 0)
        if dot1 == []:
            print "dot1 etait null"
            dot1 = [0, 0]
        if dot2 == []:
            print "dot2 etait null"
            dot2 = [iw - 1, ih - 1]

        self.image = thresh1

        cv2.line(self.image, dot1, dot2, (255, 0, 0), 2)
        cv2.line(self.image, (dot1[0], (dot1[1] + dot2[1])/2), (dot2[0], (dot1[1] + dot2[1])/2),(0, 0, 255), 2)
        distancePixel = dot1[1] - (dot1[1] + dot2[1])/2
        # print distancePixel
        return distancePixel


    def differenceParraleleLinesStation(self):
        ret,thresh1 = cv2.threshold(self.image,100,255,cv2.THRESH_BINARY)


        ih, iw, ic = self.image.shape
        col1 = 0
        col2 = iw - 1
        dot1 = []
        dot2 = []


        for i in range(0, ih):
            if np.equal(thresh1[i, 0], np.array([255,255,255])).all():
                dot1 = (0, i)
                break
            if dot1 == []:
                dot1 = (0, ih-1)

        for i in range(0, ih):
            if not np.equal(thresh1[i, col2], np.array([0,0,0])).all():
                dot2 = (col2, i)
                break
            if dot2 == []:
                for i in range(iw - 1, -1, -1):
                    if not np.equal(thresh1[ih - 1, i], np.array([0,0,0])).all():
                        dot2 = (col2, i)
                        break

        # print dot1
        # print dot2
        # dot1 = (1279, 0)
        if dot1 == []:
            print "dot1 etait null"
            dot1 = [0, 0]
        if dot2 == []:
            print "dot2 etait null"
            dot2 = [iw - 1, ih - 1]

        self.image = thresh1

        cv2.line(self.image, dot1, dot2, (255, 0, 0), 2)
        cv2.line(self.image, (dot1[0], (dot1[1] + dot2[1])/2), (dot2[0], (dot1[1] + dot2[1])/2),(0, 0, 255), 2)
        distancePixel = dot1[1] - (dot1[1] + dot2[1])/2
        # print distancePixel
        return distancePixel

    def getCloserToTreasures(self):
        findSomething = False
        movingY = False
        moveYArriver = False
        movingX = False
        moveXArriver = False
        self.tresor = None
        lastAngle= 180

        self.camera.moveCameraByAngle(1, 70)
        self.camera.moveCameraByAngle(0, 30)

        while(self.video.isOpened()):
            ret, self.image = self.video.read()
            self.detectTreasureColor()
            self.findContour()

            if not findSomething:
                findSomething = self.swipeCamera()

            if self.tresor == None:
                findSomething = False
                movingY = False
                moveYArriver = False
                movingX = False
                moveXArriver = False



            center = self.moveCamera()


            if not self.robot.isMoving and center:
                if not movingY and not moveYArriver:
                    diff = self.differenceParraleleLinesTresor()
                    if diff < 0:
                        self.robot.moveForever(0, -30)
                    else:
                        self.robot.moveForever(0, 30)
                    movingY = True

                if moveYArriver:
                    if not movingX and not moveXArriver:
                        self.robot.moveForever(30, 0)
                        movingX = True

            if movingY and not moveYArriver:
                if abs(self.differenceParraleleLinesTresor()) < 8:
                    self.robot.stopAllMotors()
                    moveYArriver = True
                    movingY = False


            if movingX and not moveXArriver:
                print self.camera.verticalDegree


                if self.camera.verticalDegree <= 7.5:
                    self.robot.stopAllMotors()
                    moveXArriver = True
                elif self.camera.verticalDegree <= (lastAngle - 0.5) and self.camera.verticalDegree >= 16:
                    print "Ajustement en Y", self.camera.verticalDegree
                    self.robot.stopAllMotors()
                    # moveXArriver = True
                    moveYArriver = False
                    movingX = False
                    lastAngle = self.camera.verticalDegree



            if moveYArriver and moveXArriver:
                print "!!! ARRIVER !!!"
                return True

            #cv2.imshow("Image", self.image)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        self.video.release()
        cv2.destroyAllWindows()

    def getCloserToChargingStation(self):
        findSomething = False
        movingY = False
        moveYArriver = False
        movingX = False
        moveXArriver = False
        self.tresor = None
        lastAngle= 180

        self.camera.moveCameraByAngle(1, 70)
        self.camera.moveCameraByAngle(0, 50)

        while(self.video.isOpened()):
            ret, self.image = self.video.read()
            self.detectChargingStationColor()
            self.findContour()

            if not findSomething:
                findSomething = self.swipeCamera()

            if self.tresor == None:
                findSomething = False
                movingY = False
                moveYArriver = False
                movingX = False
                moveXArriver = False



            center = self.moveCamera()


            if not self.robot.isMoving and center:
                if not movingY and not moveYArriver:
                    diff = self.differenceParraleleLinesStation()
                    if diff < 0:
                        self.robot.moveForever(0, -30)
                    else:
                        self.robot.moveForever(0, 30)
                    movingY = True

                if moveYArriver:
                    if not movingX and not moveXArriver:
                        self.robot.moveForever(30, 0)
                        movingX = True

            if movingY and not moveYArriver:
                if abs(self.differenceParraleleLinesStation()) < 8:
                    self.robot.stopAllMotors()
                    moveYArriver = True
                    movingY = False


            if movingX and not moveXArriver:
                print self.camera.verticalDegree


                if self.camera.verticalDegree <= 20:
                    self.robot.stopAllMotors()
                    moveXArriver = True
                elif self.camera.verticalDegree <= (lastAngle - 0.5) and self.camera.verticalDegree >= 16:
                    print "Ajustement en Y", self.camera.verticalDegree
                    self.robot.stopAllMotors()
                    # moveXArriver = True
                    moveYArriver = False
                    movingX = False
                    lastAngle = self.camera.verticalDegree



            if moveYArriver and moveXArriver:
                print "!!! ARRIVER !!!"
                return True

            # #cv2.imshow("Image", self.image)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        self.video.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    pass
    # mr = WheelManager()
    # ct = CameraTower()
    # vr = RobotVision(mr, ct)
    #
    # vr.getCloserToTreasures()
    # vr.goDetectTresorAround()
    # print("distance")
    # print(vr.DistanceAdjascentte(34))
    # vr.detecColor()
    # vr.findContour()
