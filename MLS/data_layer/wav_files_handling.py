"""
Saves measured impulse response to a mono wav file.

Function:
    saveImpulseResponseToWav(measurementResult)

Joe.
"""

import wave
import numpy

from MLS.logic_layer import player
from MLS.type_classes import type_classes


def readWavImpulseResponseFile(filename, normalize=True):
    """
    Reads an impulse response from a mono wave file.

    Joe.
    :param filename: Path and filename to wav.
    :param normalize: Normalize read data to unity. In the range [-32768, +32767] otherwise.
    :return: Vector containing wav data.
    """

    # Opens file to read from
    wf = wave.open(filename, "rb")

    # Creates output object and fills properties
    _outputIR = type_classes.ImpulseResponse()
    _outputIR.samplingFrequency = wf.getframerate()
    _outputIR.bitDepth = wf.getsampwidth() * 8

    # Reads data and saves it to output object
    _readFrames = wf.readframes(wf.getnframes())
    _outputIR.impulseResponse = player._convertStreamToChannel(_readFrames)
    if normalize:
        _outputIR.impulseResponse = numpy.divide(_outputIR.impulseResponse, float(max(_outputIR.impulseResponse)))

    # It is safer to count the length of the IR this way than using the info from WAV file
    _outputIR.lengthSamples = len(_outputIR.impulseResponse)

    return _outputIR


def saveImpulseResponseToWav(impulseResponse, filename, normalize=True):
    """
    Saves received data to Wav file.

    Joe.
    :param measurementResult: Object of type MeasurementResult containing settings and results.
    """

    _stream = player.convertChannelToStream(impulseResponse.impulseResponse, normalize)

    wf = wave.open(filename, 'w')
    wf.setnchannels(1)
    wf.setsampwidth(impulseResponse.bitDepth / 8)
    wf.setframerate(impulseResponse.samplingFrequency)
    wf.writeframes(_stream)
    wf.close()


# Code used to create an impulse response of a pure delay of 0.5 seconds
if __name__ == "__main__":
    import matplotlib.pyplot as plot

    pure_delay = [0]*44100
    pure_delay[22050] = 1

    plot.plot(pure_delay)
    plot.show()

    delay = type_classes.ImpulseResponse()
    delay.impulseResponse = pure_delay
    delay.samplingFrequency = 44100
    delay.bitDepth = 16
    delay.lengthSamples = len(pure_delay)

    saveImpulseResponseToWav(delay, "/Users/maese/Desktop/delay_ir.wav")

    delay = readWavImpulseResponseFile("/Users/maese/Desktop/delay_ir.wav")
    print delay.lengthSamples
    print delay.bitDepth
    print delay.samplingFrequency

    plot.plot(delay.impulseResponse)
    plot.show()
