"""
Handles the operations with the results from the measurement.

Joe.
"""

from MLS.data_layer import write_wav


def saveResultsToFile(measurementResult):
    """
    Saves computed impulse response to a file.

    :param measurementResult: Object type MeasurementResult with results.
    """
    write_wav.saveImpulseResponseToWav(measurementResult)
