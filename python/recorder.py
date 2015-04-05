import pyaudio
import numpy
import player


def rec(numOfChannels, recordingLength, samplFreq, bitDepth, deviceIndex=-1):
    """
    Captures signals from the default sound card.

    :param numOfChannels: Number of channels
    :param recordingLength: Duration of the recording (samples)
    :param samplFreq: Sampling frequency
    :param bitDepth: Number of bits
    :return: Recording data
    """

    # Adjusts bit depth in case it is not in the accepted range
    if bitDepth == 8:
        _sampleFormat = pyaudio.paInt8
    elif bitDepth == 16:
        _sampleFormat = pyaudio.paInt16
    else:
        _sampleFormat = pyaudio.paInt16

    # Adjusts recording length to an integer number of frames
    _bufferSize = 1024
    _realRecordingLength = int(numpy.ceil(1.0 * recordingLength / _bufferSize))*_bufferSize

    # Creates the audio recorder with given parameters
    _audioRecorder = pyaudio.PyAudio()

    # Uses device index in case it is chosen, default device otherwise
    if deviceIndex > -1:
        _recordingStream = _audioRecorder.open(format=_sampleFormat,
                                               channels=numOfChannels,
                                               rate=samplFreq,
                                               input=True,
                                               frames_per_buffer=_bufferSize,
                                               output_device_index=deviceIndex)
    else:
        _recordingStream = _audioRecorder.open(format=_sampleFormat,
                                               channels=numOfChannels,
                                               rate=samplFreq,
                                               input=True,
                                               frames_per_buffer=_bufferSize)

    # Records the necessary amount of frames
    _recordedFrames = _recordingStream.read(_realRecordingLength)

    # Converts recorded frames to 16-bit signed samples
    _outputSamples = player.convertStreamToChannels(_recordedFrames)

    return _outputSamples[0:recordingLength]
