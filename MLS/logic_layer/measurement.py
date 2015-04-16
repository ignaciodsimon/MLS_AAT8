"""
Logic layer of the system. Controls the data layer and provides the results to the interface.

Function: (measurement settings is an object of type MeasurementSettings)

    executeMeasurement(measurementSetting)

Joe.
"""


# Internal imports
import numpy

import parallel_functions
import compute_ir
import recorder
import player
import generate_mls
from MLS.type_classes import type_classes


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
    _MLSSignal = generate_mls.generateMLS(measurementSetting.MLSLength, measurementSetting.signalAmplitude)

    # Padding MLS signal with zeros at the beginning
    _MLS_WithZeros = [0] * int(round(measurementSetting.preDelayForPlayback/1000.0 * measurementSetting.outputDeviceSamplFreq)
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
        [_recorderOutputData, _playerOutputData] = parallel_functions.runInParallel(recorder.rec,
                                                                                   _recorderArguments,
                                                                                   player.playSignals,
                                                                                   _playerArguments)

        _averagedLeft = numpy.add(_averagedLeft, _recorderOutputData[0][:])
        _averagedRight = numpy.add(_averagedRight, _recorderOutputData[1][:])

    _channelL = numpy.divide(_averagedLeft, measurementSetting.numberOfAverages)
    _channelR = numpy.divide(_averagedRight, measurementSetting.numberOfAverages)

    # Padding with zeros at the end of MLS signal
    _paddedMLSSignal = [0]*(len(_channelL))
    _paddedMLSSignal[0:len(_MLSSignal)] = _MLSSignal

    _IRLeft = compute_ir.computeCircularXCorr(_channelL, _paddedMLSSignal)
    _IRRight = compute_ir.computeCircularXCorr(_channelR, _paddedMLSSignal)

    if measurementSetting.referenceSignalIsLeft:
        _corrected = compute_ir.correctSignalWithIR(inputSignal=_IRRight, referenceImpulseResponse=_IRLeft)
    else:
        _corrected = compute_ir.correctSignalWithIR(inputSignal=_IRLeft, referenceImpulseResponse=_IRRight)

    # Creates output object
    _resultData = type_classes.MeasurementResult()
    _resultData.settings = measurementSetting
    _resultData.computedImpulseResponse = _corrected
    _resultData.partialIR_Left = _IRLeft
    _resultData.partialIR_Right = _IRRight

    return _resultData
