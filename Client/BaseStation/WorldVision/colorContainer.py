from Factories.ColorFactory import ColorFactory
import numpy as np

class ColorContainer():
    colorFactory = ColorFactory()
    colors = []
    islandColors = []

    yellowTreasure = colorFactory.constructColor(np.uint8([[[162, 148, 17]]]), "YellowTreasure")
    yellowTreasureDetect = colorFactory.constructColor(np.uint8([[[162, 148, 17]]]), "YellowTreasureDetect")
    green = colorFactory.constructColor(np.uint8([[[0,255,0]]]), "Green")
    red = colorFactory.constructColor(np.uint8([[[150,179,255]]]), "Red")
    everything = colorFactory.constructColor(np.uint8([[[0,0,0]]]), "Everything")
    redProximity = colorFactory.constructColor(np.uint8([[[150,179,255]]]), "RedProximity")


    islandColors.append(colorFactory.constructColor(np.uint8([[[0,255,0]]]), "Green"))
    islandColors.append(colorFactory.constructColor(np.uint8([[[255,0,0]]]), "Blue"))
    islandColors.append(colorFactory.constructColor(np.uint8([[[150,179,255]]]), "Red"))
    islandColors.append(colorFactory.constructColor(np.uint8([[[0,255,255]]]), "Yellow"))
    colors.append(colorFactory.constructColor(np.uint8([[[0,0,0]]]), "Black"))
    colors.append(colorFactory.constructColor(np.uint8([[[0,255,0]]]), "Green"))
    colors.append(colorFactory.constructColor(np.uint8([[[255,0,0]]]), "Blue"))
    colors.append(colorFactory.constructColor(np.uint8([[[121,61,128]]]), "Purple"))
    colors.append(colorFactory.constructColor(np.uint8([[[150,179,255]]]), "Red"))
    colors.append(colorFactory.constructColor(np.uint8([[[0,255,255]]]), "Yellow"))

    def getAllColors(self):
        return self.colors

    def getIslandColors(self):
        return self.islandColors