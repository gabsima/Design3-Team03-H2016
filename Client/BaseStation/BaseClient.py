from WorldVision.worldVision import worldVision
from Logic.Sequencer import Sequencer as seq
from Logic.Pathfinding.Pathfinder import Pathfinder
import cv2
import base64

class BaseClient():
    def __init__(self):
        self.world = worldVision()

    def handleCurrentSequencerState(self, obstacleListIndex):
        return self.sequencer.handleCurrentState(obstacleListIndex)

    def initialiseWorldData(self):
        print("get map")
        map = self.world.getCurrentMap()
        print("set pathfinder")
        self.pathfinder = Pathfinder(map)
        print("set sequencer")
        self.sequencer = seq(self.pathfinder)

    def getCurrentWorldImage(self):
        image = self.world.getCurrentImage()
        convertedImage = cv2.imencode('.png',image)[1]
        base64ConvertedImage = base64.encodestring(convertedImage)
        return base64ConvertedImage
