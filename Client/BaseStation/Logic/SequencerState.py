from MapCoordinatesAjuster import MapCoordinatesAjuster

class SendingBotToChargingStationState():
    def handle(self, sequencer, map, pathfinder):
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        sequencer.setState(DetectTreasureState())
        return pathfinder.findPath(convertedPoint, (885,110)), "alignPositionToChargingStation", 270



class DetectTreasureState():
    def handle(self, sequencer, map, pathfinder):
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        sequencer.setState(SendingBotToTreasureState())
        safeSpot = pathfinder.findGoodPoint((800,250))
        return  pathfinder.findPath(convertedPoint,safeSpot), "detectTreasure", 180

class SendingBotToTreasureState():
    def handle(self, sequencer, map, pathfinder):
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        treasurePosition, orientationToGo = map.getPositionInFrontOfTreasure()
        convertedRobotPosition = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        convertedTreasurePosition = mapCoordinatesAdjuster.convertPoint(treasurePosition)
        sequencer.setState(SendingBotToTargetState())
        return  pathfinder.findPath(convertedRobotPosition, convertedTreasurePosition), "alignPositionToTreasure", orientationToGo


class SendingBotToTargetState():
    def handle(self, sequencer, map, pathfinder):
        path, orientationToGo = map.getPositionInFrontOfIsland()
        pathfinder.theGoodPath = path
        sequencer.setState(StopMovingState())
        return path, "alignPositionToTarget", orientationToGo

class StopMovingState():
    def handle(self, sequencer, map, pathfinder):
        return None, None, None

