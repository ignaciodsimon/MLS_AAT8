"""
Logic layer of the system. Controls the data layer and provides the results to the interface.

executeMeasurement(MLSLength=32768,
                       inputDeviceSamplFreq=44100,
                       outputDeviceSamplFreq=44100,
                       signalAmplitude=0.5,
                       preDelayForPlayback=0.25,
                       decayTime=5.0,
                       inputDevice=-1,
                       outputDevice=-1)

Joe.
"""


# Internal imports
import recorder
import parallelfunctions
import player
import computeIR
import generateMLS


def executeMeasurement(MLSLength=32768,
                       inputDeviceSamplFreq=44100,
                       outputDeviceSamplFreq=44100,
                       signalAmplitude=0.5,
                       preDelayForPlayback=0.25,
                       decayTime=5.0,
                       inputDevice=-1,
                       outputDevice=-1):
    """
    Logic implementation of the system. Controls the data layer and provides the results
    of the measurement.

    Joe.
    :param MLSLength: Desired length of MLS signal.
    :param inputDeviceSamplFreq: Input device sampling frequency.
    :param outputDeviceSamplFreq: Output device sampling frequency.
    :param signalAmplitude: Amplitude of MLS signal.
    :param preDelayForPlayback: Pre-delay to correct for the latency of sound card.
    :param decayTime: Decay time of system-under-test. Should be a bit larger than expected one.
    :param inputDevice: Input audio device to use, index from zero. Omit to use default device.
    :param outputDevice: Output audio device to use, index from zero. Omit to use default device.
    :return: Measured impulse response, corrected with the second channel.
    """

    # Fixed to two channels to compensate for the sound card delay and defects
    _channels = 2

    # Generate the MLS signal
    _MLSSignal = generateMLS.generateMLS(MLSLength, signalAmplitude)

    # Padding MLS signal with zeros at the beginning
    _MLS_WithZeros = [0] * int(round(preDelayForPlayback * outputDeviceSamplFreq) + MLSLength)
    _MLS_WithZeros[len(_MLS_WithZeros)-len(_MLSSignal):len(_MLS_WithZeros)] = _MLSSignal
    _MLSSignal = _MLS_WithZeros

    # Recording length is function of MLS length and the system decay time
    _recordingLength = len(_MLSSignal) + int(inputDeviceSamplFreq * decayTime)

    # Player and recorder input arguments in vectors for multitasking
    _recorderArguments = [_channels, _recordingLength, inputDeviceSamplFreq, 16, inputDevice]
    _playerArguments = [_MLSSignal, _MLSSignal, outputDeviceSamplFreq, False, outputDevice]

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
