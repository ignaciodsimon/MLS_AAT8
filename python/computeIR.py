"""
Functions for estimating impulse response from recorded signal and for correcting a signal with
a known impulse response.

Example:
    computeCircularXCorr(signalA, signalB)
    correctSignalWithIR(inputSignal, impulseResponse)

Joe.
"""

import numpy
from math import sqrt


def correctSignalWithIR(inputSignal, impulseResponse):
    """
    Corrects a recorded signal with a known impulse response. It can be used to correct for
    the possible delay and non-linear behavior of acquisition system.

    Joe.
    :param inputSignal: Signal to be corrected.
    :param impulseResponse: Known impulse response the signal was processed with.
    :return: Signal corrected (de-convolved).
    """

    # Computes FFT of input signals
    _fftSignal = numpy.fft.fft(inputSignal)
    _fftReference = numpy.fft.fft(impulseResponse)

    # Corrects module and phase
    _outputModule = numpy.true_divide(abs(_fftSignal), abs(_fftReference))
    _outputPhase = numpy.subtract(numpy.angle(_fftSignal), numpy.angle(_fftReference))

    # Computes real / imaginary parts
    _outputRealPart = numpy.multiply(_outputModule, numpy.cos(_outputPhase))
    _outputImagPart = numpy.multiply(_outputModule, numpy.sin(_outputPhase))

    _outputSpectrum = [0]*len((_outputRealPart))
    for n in range(len(_outputRealPart)-1):
        _outputSpectrum[n] = numpy.complex(_outputRealPart[n], _outputImagPart[n])

    # Returns IR of computed spectrum
    return numpy.real(numpy.fft.ifft(_outputSpectrum))


def computeRMSValue(inputSignal):
    """
    Computes the Root Mean Square value of a given signal.

    Joe.
    :param inputSignal: Vector of numbers to process.
    :return: Computed RMS value.
    """
    _computedRMSValue = sqrt(1.0 / len(inputSignal) * numpy.dot(inputSignal, inputSignal))

    return _computedRMSValue


def computeCircularXCorr(signalA, signalB):
    """
    Computes the circular cross-correlation of two signals. Supposes both signals to have the
    same length. If not, they should be padded with zeros before calling this function.

    Joe.
    :param signalA: Signal A.
    :param signalB: Signal B.
    :return:
    """

    # Normalizes smaller signal to the (bigger) other one, to avoid excessive numeric errors
    # If signal A has more power
    if computeRMSValue(signalA) > computeRMSValue(signalB):
        # Then normalize signal B
        signalB = list(numpy.multiply(signalB, float(computeRMSValue(signalA) / computeRMSValue(signalB))))
    else:
        # Otherwise normalize signal A
        signalA = list(numpy.multiply(signalA, float(computeRMSValue(signalB) / computeRMSValue(signalA))))

    # Computes circular cross-correlation using the FFT
    _circularXCorr = numpy.fft.ifft(numpy.fft.fft(signalA) * numpy.fft.fft(signalB).conj()).real

    return _circularXCorr
