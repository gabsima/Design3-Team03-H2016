class Node:
    def __init__(self, position):
        self.isASafeNode = False
        self.positionX = position.__getitem__(0)
        self.positionY = position.__getitem__(1)
        self.connectedNodes = []


    def addConnectedNode(self, nodeToBeAdd):
        self.connectedNodes.append(nodeToBeAdd)


    def getConnectedNodesList(self):
        return self.connectedNodes


