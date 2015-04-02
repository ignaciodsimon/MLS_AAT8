"""
Functions to estimate impulse response from recorded signal.

Example:
    computeCircularXCorr(signalA, signalB)


Joe.
"""

import numpy
from math import sqrt


def computeRMSValue(inputSignal):
    """
    Computes the Root Mean Square value of a given signal.

    Joe.
    :param inputSignal: Vector of numbers to process
    :return: Computed RMS value
    """
    _computedRMSValue = sqrt(1.0 / len(inputSignal) * numpy.dot(inputSignal, inputSignal))

    return _computedRMSValue


def computeCircularXCorr(signalA, signalB):
    """
    Computes the circular cross-correlation of two signals. Supposes both signals to have the
    same length. If not, they should be padded with zeros before calling this function.

    Joe.
    :param signalA:
    :param signalB:
    :return:
    """

    # Normalizes smaller signal to the (bigger) other one, to avoid excessive numeric errors
    # If signal A has more power
    if computeRMSValue(signalA) > computeRMSValue(signalB):
        # Then normalize signal B
        signalB = numpy.multiply(signalB, float(computeRMSValue(signalA) / computeRMSValue(signalB)))
    else:
        # Otherwise normalize signal A
        signalA = numpy.multiply(signalA, float(computeRMSValue(signalB) / computeRMSValue(signalA)))

    # Computes the circular cross-correlation by displacing one vector and computing the dot
    # product of the two vectors for every displacement
    _computedCircXCorr = [0]*len(signalA)
    for k in range(len(signalA)):
        _computedCircXCorr[k] = numpy.dot(signalA, signalB)

        # Rotates vector B
        signalB = signalB[1:] + signalB[:1]

    return _computedCircXCorr


import random
import matplotlib.pyplot as plot

signal1 = [random.gauss(0, 1) for n in range(4000)]
signal2 = signal1[150:] + signal1[:150]

crossCorr = computeCircularXCorr(signal2, signal1)

plot.plot(crossCorr)
plot.show()
