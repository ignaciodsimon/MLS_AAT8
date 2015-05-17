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
from MLS.data_layer import wav_files_handling


def executeMeasurement(measurementSetting):
    """
    Logic implementation of the system. Controls the data layer and provides the results
    of the measurement.

    Joe.

    :param measurementSetting: Settings to be used, object of type MeasurementSettings
    :return: Measured impulse response, corrected with the second channel.
    """

    # Fixed to two channels, multichannel is not yet supported
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
    for _i in range(measurementSetting.numberOfPreAverages):

        # Runs player and recorder simultaneously
        [_recorderOutputData, _playerOutputData] = parallel_functions.runInParallel(recorder.rec,
                                                                                    _recorderArguments,
                                                                                    player.playSignals,
                                                                                    _playerArguments)

        _averagedLeft = numpy.add(_averagedLeft, _recorderOutputData[0][:])
        _averagedRight = numpy.add(_averagedRight, _recorderOutputData[1][:])

    _channelL = numpy.divide(_averagedLeft, measurementSetting.numberOfPreAverages)
    _channelR = numpy.divide(_averagedRight, measurementSetting.numberOfPreAverages)

    # Padding with zeros at the end of MLS signal
    _paddedMLSSignal = [1]*(len(_channelL))
    _paddedMLSSignal[0:len(_MLSSignal)] = _MLSSignal

    # Computes RAW impulse responses
    _rawIRLeft = compute_ir.correctSignalWithIR(_channelL, _paddedMLSSignal)
    _rawIRRight = compute_ir.correctSignalWithIR(_channelR, _paddedMLSSignal)
    # _rawIRLeft = compute_ir.computeCircularXCorr(_channelL, _paddedMLSSignal)
    # _rawIRRight = compute_ir.computeCircularXCorr(_channelR, _paddedMLSSignal)

    # Creates output object
    _resultData = type_classes.MeasurementResult()
    _resultData.settings = measurementSetting

    # Saves RAW impulse responses
    _resultData.rawIR_Left = _rawIRLeft
    _resultData.rawIR_Right = _rawIRRight

    # Loads HW correction IR from files if necessary
    if measurementSetting.shouldUseHWCorrection:

        if measurementSetting.hwCorrectionFilename_L != "":
            print "Loading HW correction for Left channel ..."
            measurementSetting.hwCorrection_Left = wav_files_handling.\
                readWavImpulseResponseFile(measurementSetting.hwCorrectionFilename_L).impulseResponse
        if measurementSetting.hwCorrectionFilename_R != "":
            print "Loading HW correction for Right channel ..."
            measurementSetting.hwCorrection_Right = wav_files_handling.\
                readWavImpulseResponseFile(measurementSetting.hwCorrectionFilename_R).impulseResponse

    if measurementSetting.dualChannelMode:

        _resultData.outputIR_Left = _rawIRLeft
        _resultData.outputIR_Right = _rawIRRight

        # Applies HW correction if necessary
        if measurementSetting.shouldUseHWCorrection:
            # Corrects Left channel
            if measurementSetting.hwCorrection_Left is not None:
                _resultData.outputIR_Left = compute_ir.\
                    correctSignalWithIR(inputSignal=_rawIRLeft,
                                        referenceImpulseResponse=measurementSetting.hwCorrection_Left)
            # Corrects Right channel
            if measurementSetting.hwCorrection_Left is not None:
                _resultData.outputIR_Right = compute_ir.\
                    correctSignalWithIR(inputSignal=_rawIRRight,
                                        referenceImpulseResponse=measurementSetting.hwCorrection_Right)

        # Applies calibration if necessary
        if measurementSetting.calibration_Left is not None:
            _resultData.outputIR_Left = compute_ir.\
                correctSignalWithIR(inputSignal=_resultData.outputIR_Left,
                                    referenceImpulseResponse=measurementSetting.calibration_Left)
        if measurementSetting.calibration_Right is not None:
            _resultData.outputIR_Right = compute_ir.\
                correctSignalWithIR(inputSignal=_resultData.outputIR_Right,
                                    referenceImpulseResponse=measurementSetting.calibration_Right)
    else:
        # Uses one channel as compensation for the other
        if measurementSetting.referenceSignalIsLeft:
            _resultData.outputIR_Left = compute_ir.correctSignalWithIR(inputSignal=_rawIRRight,
                                                                       referenceImpulseResponse=_rawIRLeft)
        else:
            _resultData.outputIR_Left = compute_ir.correctSignalWithIR(inputSignal=_rawIRLeft,
                                                                       referenceImpulseResponse=_rawIRRight)

        # If necessary, applies calibration to the output (Left output used in single mode)
        if measurementSetting.calibration_Left is not None:

            # Normalizes the IR before applying calibration

            # _resultData.outputIR_Left = numpy.divide(_resultData.outputIR_Left, max(_resultData.outputIR_Left))

            # Corrects the output with the calibration
            _resultData.outputIR_Left = compute_ir.\
                correctSignalWithIR(inputSignal=_resultData.outputIR_Left,
                                    referenceImpulseResponse=measurementSetting.calibration_Left)

        _resultData.outputIR_Right = None

    return _resultData
