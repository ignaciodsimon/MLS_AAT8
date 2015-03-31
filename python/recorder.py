import pyaudio
import numpy
import matplotlib.pyplot as plot

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


    print("* recording")

    frames = []


    for i in range(0, int(_fs / buffer * (_duration/_fs))):
        data = stream.read(buffer)
        x = numpy.fromstring(data, numpy.int16)  # convert to ints
        frames.append(x) # 2 bytes(16 bits) per channel
        x.tostring()  # convert back to data stream

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()


    plot.plot(frames)
    plot.show()

    return(frames)


if __name__ == '__main__':

    print('Acquiring recording settings:')
    print('Enter number of channels:')
    channels = input()
    print('Enter duration(samples):')
    duration = input()
    print('Enter sampling frequency:')
    fs = input()
    print('Enter number of bits:')
    nbits = input()

    rec(channels,duration,fs,nbits)
