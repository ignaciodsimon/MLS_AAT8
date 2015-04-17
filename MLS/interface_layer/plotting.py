"""
Function for plotting measured impulse response. Opens plot in a new window.

Function:
    plotResults(measurementResult)

Joe.
"""


import numpy
import matplotlib.pyplot as plot
from MLS import language_strings


def plotResults(measurementResult):
    """
    Creates a basic plot window of the given impulse response.
    Should be modified and improved, to include a window with controls for displaying different types of plots.

    Joe.
    :param measurementResult: Object received as a result when performing a measurement.
    """

    if measurementResult.settings.dualChannelMode:
        plot.subplot(2, 1, 1)

        if measurementResult.settings.normalizeOutput:
            _leftChannelPlotSignal = numpy.divide(measurementResult.outputIR_Left,
                                                  max(numpy.abs(measurementResult.outputIR_Left)))
        else:
            _leftChannelPlotSignal = measurementResult.outputIR_Left

        plot.plot(_leftChannelPlotSignal)
        plot.ylabel(language_strings.TEXT_34 + " - L")
        plot.title(language_strings.TEXT_35)
        plot.grid()

        plot.subplot(2, 1, 2)

        if measurementResult.settings.normalizeOutput:
            _rightChannelPlotSignal = numpy.divide(measurementResult.outputIR_Right,
                                                   max(numpy.abs(measurementResult.outputIR_Right)))
        else:
            _rightChannelPlotSignal = measurementResult.outputIR_Right

        plot.plot(_rightChannelPlotSignal)
        plot.xlabel(language_strings.TEXT_33)
        plot.ylabel(language_strings.TEXT_34 + " - R")
        plot.grid()

    else:
        plot.plot(measurementResult.outputIR_Left)
        plot.xlabel(language_strings.TEXT_33)
        plot.ylabel(language_strings.TEXT_34)
        plot.title(language_strings.TEXT_35)
        plot.grid()

    plot.show()
