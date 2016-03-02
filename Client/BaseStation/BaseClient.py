import base64
import json
import sys
import os
from Logic.Sequencer import Sequencer as seq
from WorldVision.worldVision import worldVision
import Shared.Utils as Utils

sequencer = seq()

from socketIO_client import SocketIO

c = os.path.dirname(__file__)
configPath = os.path.join(c, "..", "..", "Shared", "config.json")
picturePath = os.path.join(c, "..", "..", "Shared", "worldImage.jpg")

with open(configPath) as json_data_file:
    config = json.load(json_data_file)

socketIO = SocketIO(config['url'], int(config['port']))

def sendNextCoordinates(*args):
    print("Sending next coordinates")
    socketIO.emit("sendNextCoordinates", sequencer.handleCurrentState(args[0]["index"]))

def startRound():
    botState = {"positionX":"0",
                "positionY":"0",
                "orientation":"0"}
    print("sending start signal robot")
    socketIO.emit("startSignalRobot",botState)

def sendImage():
    print("asking for new images")
    world = worldVision()
    world.saveImage()

    encoded = base64.b64encode(open(picturePath, "rb").read())
    socketIO.emit('sendImage', encoded)

Utils.setInterval(sendImage, 5)
socketIO.on('needNewCoordinates', sendNextCoordinates)
socketIO.on('startSignal', startRound)

socketIO.wait()

