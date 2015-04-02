import pyaudio
import numpy


def twosComplementToInt(msb, lsb):
    """
    Converts a number in two 8-bit (two-complement) to a signed 16-bit integer.

    Joe.
    :param msb: High 8-bit
    :param lsb: Low 8-bit
    :return: Signed 16-bit integer
    """

    # Counts the two parts of the number
    number = msb*256 + lsb

    # Corrects the sign if necessary
    if msb > 127:
        number -= 65536

    return number


def intToTwosComplement(inputNumber):
    """
    Converts a signed 16-bit number to two 8-bit registers in two-complement.

    Joe.
    :param inputNumber: Signed 16-bit to convert
    :return: 8-bit registers in order: [msb, lsb]
    """

    msb = int(abs(inputNumber) / 256)
    lsb = abs(inputNumber) - (msb*256)
    if inputNumber < 0:
        msb = 255 - msb
        lsb = 255 - lsb

    return [msb, lsb]


def convertStreamToChannels(stereoStream):
    """
    Converts a two channel stream in 8-bit 2-complement format to two vectors
    of 16-bit numbers. This type of 8-bit stream is used when recording / playing
    back signals using the sound card.

    Joe.
    :param stereoStream: 8-bit 2-complement data to convert
    :return: Separated channels in format: [[L1 L2 L3 ...], [R1 R2 R3 ...]]
    """

    channelL = [0]*(len(stereoStream)/4)
    channelR = [0]*(len(stereoStream)/4)
    sampIndex = 0
    for n in range(0, len(stereoStream)-4, 4):

        channelL[sampIndex] = twosComplementToInt(ord(stereoStream[n+1]), ord(stereoStream[n]))
        channelR[sampIndex] = twosComplementToInt(ord(stereoStream[n+3]), ord(stereoStream[n+2]))

        sampIndex += 1

    return [channelL, channelR]


def convertChannelsToStream(channelL, channelR, normalize=False):
    """
    Converts two 16-bit audio signals to a wav-type stream (8-bit two-complement interleaved
    samples).

    Joe.
    :param channelL: Left audio signal (signed 16-bit float)
    :param channelR: Left audio signal (signed 16-bit float)
    :param normalize: Should normalize input signals to fill the dynamic range
    :return: Wav-type interleaved stream
    """

    # Calculates normalization value
    if normalize:
        normalizationValue = max(max(channelL), max(channelR))
    else:
        normalizationValue = 1.0

    outputStream = ''
    for n in range(len(channelL)):

        # Adapts input signals (signed float) to 16-bit signed integer range
        currentLSample = int(channelL[n] * float(pow(2, 16))/2 / normalizationValue)
        currentRSample = int(channelR[n] * float(pow(2, 16))/2 / normalizationValue)

        samplesL = intToTwosComplement(currentLSample)
        samplesR = intToTwosComplement(currentRSample)

        outputStream = outputStream + chr(samplesL[1]) + chr(samplesL[0])
        outputStream = outputStream + chr(samplesR[1]) + chr(samplesR[0])

    return outputStream


def playSignals(signalLeft, signalRight, samplingFreq=44100, normalize=False):
    """
    Plays input signals to sound card using the PyAudio library. Input signals are expected
    as float vectors.

    Note: if normalization is disabled, signals must not exceed unity amplitude to prevent
    saturation.

    Joe.
    :param signalLeft: Signal to left output of sound card.
    :param signalRight: Signal to right output of sound card.
    :param normalize: Should normalize input signals
    :return:
    """
    # Creates audio player
    p = pyaudio.PyAudio()

    # Configures audio player with input parameters
    stream = p.open(format=p.get_format_from_width(2),
                    channels=2,
                    rate=samplingFreq,
                    output=True)

    # Converts input signals to Wav stream
    signalStream = convertChannelsToStream(signalLeft, signalRight, normalize)

    # Sends stream to audio player
    stream.write(signalStream)

    # Stop, close and free
    stream.stop_stream()
    stream.close()
    p.terminate()


# # --== Complete recording code ==--
#
# # Creates audio recorder
# p = pyaudio.PyAudio()
#
# # Opens audio recorder with parameters
# stream = p.open(format=pyaudio.paInt16,
#                 channels=2,
#                 rate=44100,
#                 input=True,
#                 frames_per_buffer=1024)
#
#
# data = stream.read(1024*5)
#
# myLeft = []
# myRight = []
#
# [myLeft, myRight] = convertStreamToChannels(data)
#
# plot.plot(myRight)
# plot.show()
#
# stream.stop_stream()
# stream.close()
# p.terminate()


# --== Complete playback code ==--

# Generates the signals
signal1 = [1.0 * numpy.sin(2 * numpy.pi * 1000 * n/44100) for n in range(44100)]
signal2 = [1.0 * numpy.sin(2 * numpy.pi * 2000 * n/44100) for n in range(44100)]

# Sends them to the sound card
playSignals(signal1, signal2, samplingFreq=44100, normalize=False)
