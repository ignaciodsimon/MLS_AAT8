import matplotlib.pyplot as plot


def plotResults(measurementResult):
    plot.plot(measurementResult.computedImpulseResponse)
    plot.show()
