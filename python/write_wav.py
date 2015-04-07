"""
Saves measured impulse response to a mono wav file.

Function:
    saveImpulseResponseToWav(measurementResult)

"""


import player
import wave


def saveImpulseResponseToWav(measurementResult):
    """
    Saves received data to Wav file.

    Joe.
    :param measurementResult: Object of type MeasurementResult containing settings and results.
    """

    _stream = player.convertChannelToStream(measurementResult.computedImpulseResponse,
                                            measurementResult.settings.normalizeOutput)

    wf = wave.open(measurementResult.settings.shouldSaveToFileFilename, 'w')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(measurementResult.settings.inputDeviceSamplFreq)
    wf.writeframes(_stream)
    wf.close()
