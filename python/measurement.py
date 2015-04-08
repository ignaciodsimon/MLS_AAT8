"""
Logic layer of the system. Controls the data layer and provides the results to the interface.

Function: (measurement settings is an object of type MeasurementSettings)

    executeMeasurement(measurementSetting)

Also holds two public classes:

    class MeasurementSettings
    class MeasurementResult

Joe.
"""


# Internal imports
import recorder
import parallelfunctions
import player
import computeIR
import generateMLS
import numpy


class MeasurementSettings:
    """
    Measurement settings definition class. Used to provide information of measurement to be performed.

    Public fields:

    MLSLength: Desired length of MLS signal.
    inputDeviceSamplFreq: Input device sampling frequency.
    outputDeviceSamplFreq: Output device sampling frequency.
    signalAmplitude: Amplitude of MLS signal.
    preDelayForPlayback: Pre-delay to correct for the latency of sound card.
    decayTime: Decay time of system-under-test. Should be a bit larger than expected one.
    inputDevice: Input audio device to use, index from zero. Omit to use default device.
    outputDevice: Output audio device to use, index from zero. Omit to use default device.

    Joe.
    """

    # Class constructor
    def __init__(self):
        self.data = []

    # Public fields
    MLSLength = 32768
    inputDeviceSamplFreq = 44100
    outputDeviceSamplFreq = 44100
    signalAmplitude = 0.5
    preDelayForPlayback = 0.25
    decayTime = 5.0
    inputDevice = -1
    outputDevice = -1
    normalizeOutput = 1

    shouldPlot = False
    shouldSaveToFile = False
    shouldSaveToFileFilename = ""

    numberOfAverages = 3


class MeasurementResult:
    """
    Measurement results definition class. Used to return information of performed measurement.

    Joe.
    """

    # Class constructor
    def __init__(self):
        self.data = []

    # Public fields
    settings = 0
    computedImpulseResponse = 0


def executeMeasurement(measurementSetting):
    """
    Logic implementation of the system. Controls the data layer and provides the results
    of the measurement.

    Joe.

    :param measurementSetting: Settings to be used, object of type MeasurementSettings
    :return: Measured impulse response, corrected with the second channel.
    """

    # Fixed to two channels to compensate for the sound card delay and defects
    _channels = 2

    # Generate the MLS signal
    _MLSSignal = generateMLS.generateMLS(measurementSetting.MLSLength, measurementSetting.signalAmplitude)

    # Padding MLS signal with zeros at the beginning
    _MLS_WithZeros = [0] * int(round(measurementSetting.preDelayForPlayback * measurementSetting.outputDeviceSamplFreq)
                               + measurementSetting.MLSLength)
    _MLS_WithZeros[len(_MLS_WithZeros)-len(_MLSSignal):len(_MLS_WithZeros)] = _MLSSignal
    _MLSSignal = _MLS_WithZeros

    # Recording length is function of MLS length and the system decay time
    _recordingLength = len(_MLSSignal) + int(measurementSetting.inputDeviceSamplFreq * measurementSetting.decayTime)

    # Normalizing the recording length to an integer number of frames
    _recordingLength = int(1024 * numpy.ceil(float(_recordingLength) / float(1024)))

    # Player and recorder input arguments in vectors for multitasking
    _recorderArguments = [_channels, _recordingLength, measurementSetting.inputDeviceSamplFreq,
                          16, measurementSetting.inputDevice]
    _playerArguments = [_MLSSignal, _MLSSignal, measurementSetting.outputDeviceSamplFreq,
                        False, measurementSetting.outputDevice]


    _averagedLeft = [0] * _recordingLength
    _averagedRight = [0] * _recordingLength
    for _i in range(measurementSetting.numberOfAverages):

        # Runs player and recorder simultaneously
        [_recorderOutputData, _playerOutputData] = parallelfunctions.runInParallel(recorder.rec,
                                                                                   _recorderArguments,
                                                                                   player.playSignals,
                                                                                   _playerArguments)

        _averagedLeft = numpy.add(_averagedLeft, _recorderOutputData[0][:])
        _averagedRight = numpy.add(_averagedRight, _recorderOutputData[1][:])

    _channelL = numpy.divide(_averagedLeft, measurementSetting.numberOfAverages)
    _channelR = numpy.divide(_averagedRight, measurementSetting.numberOfAverages)

    # Padding with zeros of MLS signal
    _paddedMLSSignal = [0]*(len(_channelL))
    _paddedMLSSignal[0:len(_MLSSignal)] = _MLSSignal

    _IRLeft = computeIR.computeCircularXCorr(_channelL, _paddedMLSSignal)
    _IRRight = computeIR.computeCircularXCorr(_channelR, _paddedMLSSignal)
    _corrected = computeIR.correctSignalWithIR(_IRLeft, _IRRight)

    # Creates output object
    _resultData = MeasurementResult()
    _resultData.settings = measurementSetting
    _resultData.computedImpulseResponse = _corrected

    return _resultData
