import pyaudio
import numpy
import player


def rec(_channels ,_duration, _fs, _nbits):
    """
    Records a signal from the microphone

    :param _channels: Number of channels
    :param _duration: Duration of the recording (samples)
    :param _fs: Sampling frequency
    :param _nbits: Number of bits
    :return: Recording data
    """

    if _nbits == 8:
        FORMAT = pyaudio.paInt8
    elif _nbits == 16:
        FORMAT = pyaudio.paInt16
    else: FORMAT = pyaudio.paInt16


    p = pyaudio.PyAudio()
    buffer = 1024
    stream = p.open(format=FORMAT,
                    channels=_channels,
                    rate=_fs,
                    input=True,
                    frames_per_buffer=buffer)

    frames = []

    for i in range(0, int(_fs / buffer * (_duration/_fs))):
        data = stream.read(buffer)
        twos = numpy.fromstring(data, numpy.int16)  # convert to ints
        x = player.twosComplementToInt(twos[i+1], twos[i])
        frames.append(x) # 2 bytes(16 bits) per channel
        twos.tostring()  # convert back to data stream

    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames