"""
Logic layer of the system. Controls the data layer and provides the results to the interface.

executeMeasurement(_MLSLength=32768,
                       _samplFreq = 44100,
                       _signalAmplitude = 0.5,
                       _preDelayForPlayback = 0.25,
                       _decayTime = 5.0)

Joe.
"""


# Internal imports
import recorder
import parallelfunctions
import player
import computeIR
import generateMLS


def executeMeasurement(_MLSLength=32768,
                       _samplFreq = 44100,
                       _signalAmplitude = 0.5,
                       _preDelayForPlayback = 0.25,
                       _decayTime = 5.0):
    """
    Logic implementation of the system. Controls the data layer and provides the results
    of the measurement.

    Joe.
    :param _MLSLength: Desired length of MLS signal.
    :param _samplFreq: Sampling frequency.
    :param _signalAmplitude: Amplitude of MLS signal.
    :param _preDelayForPlayback: Pre-delay to correct for the latency of sound card.
    :param _decayTime: Decay time of system-under-test. Should be a bit larger than expected one.
    :return: Measured impulse response, corrected with the second channel.
    """

    # Fixed to two channels to compensate for the sound card delay and defects
    _channels = 2

    # Generate the MLS signal
    _MLSSignal = generateMLS.generateMLS(_MLSLength, _signalAmplitude)

    # Padding MLS signal with zeros at the beginning
    _MLS_WithZeros = [0] * int(round(_preDelayForPlayback * _samplFreq) + _MLSLength)
    _MLS_WithZeros[len(_MLS_WithZeros)-len(_MLSSignal):len(_MLS_WithZeros)] = _MLSSignal
    _MLSSignal = _MLS_WithZeros

    # Recording length is function of MLS length and the system decay time
    _recordingLength = len(_MLSSignal) + int(_samplFreq * _decayTime)

    # Player and recorder input arguments in vectors for multitasking
    _recorderArguments = [_channels, _recordingLength, _samplFreq, 16]
    _playerArguments = [_MLSSignal, _MLSSignal, _samplFreq, False]

    # Runs player and recorder simultaneously
    [_recorderOutputData, _playerOutputData] = parallelfunctions.runInParallel(recorder.rec, _recorderArguments, player.playSignals, _playerArguments)

    # Computes IR
    channelL = _recorderOutputData[0][:]
    channelR = _recorderOutputData[1][:]

    # Padding with zeros of MLS signal
    _paddedMLSSignal = [0]*(len(channelL))
    _paddedMLSSignal[0:len(_MLSSignal)] = _MLSSignal

    _IRLeft = computeIR.computeCircularXCorr(channelL, _paddedMLSSignal)
    _IRRight = computeIR.computeCircularXCorr(channelR, _paddedMLSSignal)
    _corrected = computeIR.correctSignalWithIR(_IRLeft, _IRRight)

    return _corrected
