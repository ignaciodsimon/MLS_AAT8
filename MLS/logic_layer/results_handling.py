"""
Handles the operations with the results from the measurement.

Joe.
"""

from MLS.data_layer import wav_files_handling
from MLS.type_classes import type_classes


def saveResultsToFile(measurementResult):
    """
    Saves computed impulse response to a file.

    :param measurementResult: Object type MeasurementResult with results.
    """

    # TODO: esto es un apano, el objeto ImpulseResponse debe crearse en Measurement, no aqui

    if measurementResult.settings.dualChannelMode:

        # Creates the two different file names with "_L" and "_R" at the end of the name before the ".wav"
        if len(measurementResult.settings.shouldSaveToFileFilename) > 4 and \
                measurementResult.settings.shouldSaveToFileFilename[len(measurementResult.settings.shouldSaveToFileFilename)-4:]:
            _leftIRFilename = measurementResult.settings.shouldSaveToFileFilename[0:len(measurementResult.settings.shouldSaveToFileFilename)-4] + "_L" + measurementResult.settings.shouldSaveToFileFilename[len(measurementResult.settings.shouldSaveToFileFilename)-4:]
            _rightIRFilename = measurementResult.settings.shouldSaveToFileFilename[0:len(measurementResult.settings.shouldSaveToFileFilename)-4] + "_R" + measurementResult.settings.shouldSaveToFileFilename[len(measurementResult.settings.shouldSaveToFileFilename)-4:]
        else:
            _leftIRFilename = measurementResult.settings.shouldSaveToFileFilename + "_L.wav"
            _rightIRFilename = measurementResult.settings.shouldSaveToFileFilename + "_L.wav"

        wav_files_handling.saveImpulseResponseToWav(type_classes.ImpulseResponse(measurementResult.outputIR_Left),
                                                    _leftIRFilename,
                                                    measurementResult.settings.normalizeOutput)

        wav_files_handling.saveImpulseResponseToWav(type_classes.ImpulseResponse(measurementResult.outputIR_Right),
                                                    _rightIRFilename,
                                                    measurementResult.settings.normalizeOutput)
    else:
        wav_files_handling.saveImpulseResponseToWav(type_classes.ImpulseResponse(measurementResult.outputIR_Left),
                                                    measurementResult.settings.shouldSaveToFileFilename,
                                                    measurementResult.settings.normalizeOutput)
