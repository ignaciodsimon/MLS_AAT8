"""
Function for plotting measured impulse response. Opens plot in a new window.

Function:
    plotResults(measurementResult)

Joe.
"""


import matplotlib.pyplot as plot
from MLS import language_strings


def plotResults(measurementResult):
    """
    Creates a basic plot window of the given impulse response.
    Should be modified and improved, to include a window with controls for displaying different types of plots.

    Joe.
    :param measurementResult: Object received as a result when performing a measurement.
    """
    plot.plot(measurementResult.computedImpulseResponse)
    plot.xlabel(language_strings.TEXT_33)
    plot.ylabel(language_strings.TEXT_34)
    plot.title(language_strings.TEXT_35)
    plot.grid()
    plot.show()
