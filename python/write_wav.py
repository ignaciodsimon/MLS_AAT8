import player
import wave


def saveImpulseResponseToWav(impulseResponse, samplingFreq, outputWavFilename, normalize=False):
    """
    Saves received data to Wav file.

    Joe.
    :param impulseRespone: Computed impulse response vector.
    :param samplingFreq: Sampling frequency used (to save in Wav file).
    :param outputWavFilename: Filename (with path) to save file in.
    :param normalize: Should normalize to -3 dBFS.
    """

    _stream = player.convertChannelToStream(impulseResponse, normalize)

    wf = wave.open(outputWavFilename, 'w')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(samplingFreq)
    wf.writeframes(_stream)
    wf.close()
