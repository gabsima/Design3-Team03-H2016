class PixelToCentimeterConverter:
    RATIO = (45/9.5)

    def convertPixelToCentimeter(self, pointToBeConverted):
        pointConverted = (float(pointToBeConverted[0])/self.RATIO, float(pointToBeConverted[1])/self.RATIO)
        return pointConverted