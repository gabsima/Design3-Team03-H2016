import json

from socketIO_client import SocketIO
from Logic.RobotMock import RobotMock

with open("../../Shared/config.json") as json_data_file:
    config = json.load(json_data_file)
socketIO = SocketIO(config['url'], int(config['port']))

robot = RobotMock()
def needNewCoordinates(*args):
    print("Bot going to " + args[0]["type"] + " at : (" + args[0]["position"]["positionX"] + " " + args[0]["position"]["positionY"] + ")")
    robot.moveTo((int(args[0]["position"]["positionX"]), int(args[0]["position"]["positionY"])))
    if(args[0]["type"] == "target"):
        robot.botInfo = {"voltage" : "N/A",
                        "decodedCharacter" : "N/A",
                        "target" : "N/A"}
        socketIO.emit('sendingEndSignal')
    else:
        robot.botInfo['voltage'] = "12V"
        robot.botInfo['decodedCharacter'] = "A"
        robot.botInfo['target'] = "cercle"
        socketIO.emit('needNewCoordinates')

def sendInfo():
    socketIO.emit('sendingInfo', robot.botInfo)

socketIO.emit('sendingBotClientStatus','Connected')
socketIO.on('needUpdatedInfo', sendInfo)
socketIO.on('sendingNextCoordinates', needNewCoordinates)

socketIO.wait()




