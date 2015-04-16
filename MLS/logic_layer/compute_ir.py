"""
Functions for estimating impulse response from recorded signal and for correcting a signal with
a known impulse response.

Functions:
    computeCircularXCorr(signalA, signalB)
    correctSignalWithIR(inputSignal, impulseResponse)

Joe.
"""

import numpy
from math import sqrt


def correctSignalWithIR(inputSignal, referenceImpulseResponse):
    """
    Corrects a recorded signal with a known impulse response. It can be used to correct for
    the possible delay and non-linear behavior of acquisition system.

    Joe.
    :param inputSignal: Signal to be corrected.
    :param referenceImpulseResponse: Known impulse response the signal was processed with.
    :return: Signal corrected (de-convolved).
    """

    # Computes FFT of input signals
    _fftSignal = numpy.fft.fft(inputSignal)
    _fftReference = numpy.fft.fft(referenceImpulseResponse)

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


def _computeRMSValue(inputSignal):
    """
    Computes the Root Mean Square value of a given signal.

    Joe.
    :param inputSignal: Vector of numbers to process.
    :return: Computed RMS value.
    """
    _computedRMSValue = sqrt(1.0 / len(inputSignal) * numpy.dot(inputSignal, inputSignal))

    return _computedRMSValue


def computeCircularXCorr(signalA, signalB, frequencyBinsFactor=1):
    """
    Computes the circular cross-correlation of two signals. Supposes both signals to have the
    same length. If not, they should be padded with zeros before calling this function.

    Joe.
    :param signalA: Signal A.
    :param signalB: Signal B.
    :return: Computed circular cross-correlation.
    """

    # Normalizes smaller signal to the (bigger) other one, to avoid excessive numeric errors
    # If signal A has more power
    if _computeRMSValue(signalA) > _computeRMSValue(signalB):
        # Then normalize signal B
        signalB = list(numpy.multiply(signalB, float(_computeRMSValue(signalA) / _computeRMSValue(signalB))))
    else:
        # Otherwise normalize signal A
        signalA = list(numpy.multiply(signalA, float(_computeRMSValue(signalB) / _computeRMSValue(signalA))))

    # Computes circular cross-correlation using the FFT

    _fftLength = len(signalA) * frequencyBinsFactor

    _spectrumA = numpy.fft.fft(signalA, _fftLength)
    _spectrumB = numpy.fft.fft(signalB, _fftLength)

    _spectrumProduct = _spectrumA * _spectrumB.conj()
    _circularXCorr = numpy.fft.ifft(_spectrumProduct, _fftLength).real

    return _circularXCorr


def computeManualCircularXCorrWithDisplacement(signalA, signalB):
    """
    Computes the circular cross-correlation using the manual vector-displacement method. It results in a much slower
    way of doing it.

    Joe.
    :param signalA: Input signal A.
    :param signalB: Input signal B.
    :return: Computed circular cross-correlation.
    """

    _sequenceLength = len(signalA)

    _circularXCorr = [0]*_sequenceLength
    _tempRegistry = [0]*_sequenceLength

    for k in range(_sequenceLength):
        _tempRegistry[0:_sequenceLength-k] = signalB[k:]
        _tempRegistry[_sequenceLength-k:] = signalB[0:k]
        _circularXCorr[k] = numpy.dot(signalA, _tempRegistry)

    return _circularXCorr


def computeManualCircularXCorrWithoutDisplacement(signalA, signalB):
    """
    Computes circular cross-correlation by manually multiplying each value of the input vectors, but
    without displacing and saving a new vector every time. It results in a much slower way of doing it.

    Joe.
    :param signalA: Input signal A.
    :param signalB: Input signal B.
    :return: Computed circular cross-correlation.
    """

    _sequenceLength = len(signalA)
    _computedXCorr = [0]*_sequenceLength

    for _n in range(_sequenceLength):
        for _m in range(_sequenceLength):
            if _m+_n >= _sequenceLength:
                _computedXCorr[_n] += signalA[_m] * signalB[_m+_n-_sequenceLength]
            else:
                _computedXCorr[_n] += signalA[_m] + signalB[_m+_n]

    return _computedXCorr


"""
The following code is used to test the different methods for computing circular cross-correlation.
It also provides some estimations on the SNR that can be obtained from the methods.

Joe.
"""
if __name__ == "__main__":
    import random
    from datetime import datetime

    signalLength = int(44100 * 0.5)
    total_signal = [random.gauss(0, 1) for n in range(signalLength)]
    signalA = total_signal[0: int(0.8 * signalLength)]
    signalB = total_signal[int(0.2 * signalLength): signalLength]
    print "Sizes:", len(signalA), len(signalB)

    print "Testing mode 'Manual #1'..."
    # For one second of audio: 114.634(s)
    # For half second of audio: 28.467(s)  <-- complexity is square
    # For 5 seconds, should take: 5^2 * 114.634 = 2850(s) = 47.5 minutes
    _timeBefore = datetime.now()
    output1 = computeManualCircularXCorrWithDisplacement(signalA, signalB)
    _timeAfter = datetime.now()
    _timeDifference = _timeAfter - _timeBefore
    print _timeDifference.total_seconds()
    print "  Done ..."

    print "Testing mode 'Manual #2'..."
    # For half second of audio: 91.902(s)
    # For quarter of second of audio: 25.195(s)
    _timeBefore = datetime.now()
    output2 = computeManualCircularXCorrWithoutDisplacement(signalA, signalB)
    _timeAfter = datetime.now()
    _timeDifference = _timeAfter - _timeBefore
    print _timeDifference.total_seconds()
    print "  Done ..."

    print "Testing mode 'FFT Normal' ..."
    # For half second of audio: 0.006542(s)
    # For five seconds of audio: 0.208532(s)
    # For fifty seconds of audio: 2.111742(s)
    _timeBefore = datetime.now()
    output3 = computeCircularXCorr(signalB, signalA, frequencyBinsFactor=1)
    _timeAfter = datetime.now()
    _timeDifference = _timeAfter - _timeBefore
    print _timeDifference.total_seconds()
    print "  Done ..."

    print "Testing mode 'FFT Oversampled' ..."
    # For half second of audio: 0.006542(s)
    _timeBefore = datetime.now()
    output4 = computeCircularXCorr(signalB, signalA, frequencyBinsFactor=100)
    _timeAfter = datetime.now()
    _timeDifference = _timeAfter - _timeBefore
    print _timeDifference.total_seconds()
    print "  Done ..."

    print "Computing SNR for each case ..."
    import operator
    peakIndex1, peakValue1 = max(enumerate(output1), key=operator.itemgetter(1))
    noise1 = output1
    noise1[peakIndex1] = 0
    print "  SNR mode 1:", 20*numpy.log10(peakValue1 / _computeRMSValue(noise1))

    peakIndex2, peakValue2 = max(enumerate(output2), key=operator.itemgetter(1))
    noise2 = output2
    noise2[peakIndex2] = 0
    print "  SNR mode 2:", 20*numpy.log10(peakValue2 / _computeRMSValue(noise2))

    peakIndex3, peakValue3 = max(enumerate(output3), key=operator.itemgetter(1))
    noise3 = output3
    noise3[peakIndex3] = 0
    print "  SNR mode FFT short:", 20*numpy.log10(peakValue3 / _computeRMSValue(noise3))

    peakIndex4, peakValue4 = max(enumerate(output4), key=operator.itemgetter(1))
    noise4 = output4
    noise4[peakIndex4] = 0
    print "  SNR mode FFT long:", 20*numpy.log10(peakValue4 / _computeRMSValue(noise4))

    # import matplotlib.pyplot as plot
    # plot.subplot(3, 1, 1)
    # plot.plot(output1)
    # plot.xlabel("Method manual 1")
    # plot.subplot(3, 1, 2)
    # plot.plot(output2)
    # plot.xlabel("Method manual 2")
    # plot.subplot(3, 1, 3)
    # plot.plot(output3)
    # plot.xlabel("Method FFT")
    # plot.show()

    # Results:
    #
    # With: 1 and 100, delta = 20.02 dB
    # SNR mode FFT short: 49.9386764792
    # SNR mode FFT long: 69.9593172562
    #
    # With: 1 and 200, delta = 23.01
    # SNR mode FFT short: 49.979715978
    # SNR mode FFT long: 72.996470937
    # This means that we gain 3dB every time we double the "oversampling" of frequency bins
    #
    # The basic SNR is ~10*log10(signalLength)
    # and then it grows with the oversampling as: 10 * log10(oversampling)
