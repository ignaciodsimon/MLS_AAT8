"""
Function for plotting measured impulse response. Opens plot in a new window.

Function:
    plotResults(measurementResult)

"""


import matplotlib.pyplot as plot
from .. import language_strings


def plotResults(measurementResult):
    plot.plot(measurementResult.computedImpulseResponse)
    plot.xlabel(language_strings.TEXT_33)
    plot.ylabel(language_strings.TEXT_34)
    plot.title(language_strings.TEXT_35)
    plot.grid()
    plot.show()
