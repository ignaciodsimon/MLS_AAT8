"""
Function for plotting measured impulse response. Opens plot in a new window.

Function:
    plotResults(measurementResult)

"""


import matplotlib.pyplot as plot
import strings


def plotResults(measurementResult):
    plot.plot(measurementResult.computedImpulseResponse)
    plot.xlabel(strings.TEXT_33)
    plot.ylabel(strings.TEXT_34)
    plot.title(strings.TEXT_35)
    plot.grid()
    plot.show()
