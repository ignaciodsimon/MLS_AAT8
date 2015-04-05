"""
Functions to obtain information of all available audio devices.
Returned data is a vector of objects of type SoundCard.

    SoundCard[] = getAllSoundCardsInfo()


Joe.
"""


import pyaudio


class SoundCard:
    """
    Sound card definition class. Used to provide information about audio interfaces.

    Joe.
    """

    # Class constructor
    def __init__(self):
        self.data = []

    # Public 'fields'
    interfaceID = -1
    interfaceName = ""
    isDefaultInputInterface = False
    isDefaultOutputInterface = False
    countOfInputChannels = -1
    countOfOutputChannels = -1
    samplingRates = -1
    bitDepths = -1
    inputLatency = -1
    outputLatency = -1


def countSoundCards():
    """
    Returns the amount of available audio devices.

    Joe.
    :return: Amount of audio devices.
    """

    _devices = pyaudio.PyAudio()
    return _devices.get_device_count()


def getAllSoundCardsInfo():
    """
    Returns the information on all available audio devices. Returned information uses
    the class "SoundCard".

    Joe.
    :return: All available devices as a vector of type SoundCard[]
    """

    _soundCards = []
    _devices = pyaudio.PyAudio()

    for n in range(countSoundCards()):

        # Gets an available audio device
        _currentDevice = _devices.get_device_info_by_index(n)
        _currentSoundCard = SoundCard()

        # Bit depth is expressed in number of bytes (8 bits per byte)
        _currentSoundCard.bitDepths = _currentDevice.get("structVersion", -1)
        if _currentSoundCard.bitDepths != 0:
            _currentSoundCard.bitDepths *= 8

        # Extracts information of current device
        _currentSoundCard.countOfInputChannels = _currentDevice.get("maxInputChannels", -1)
        _currentSoundCard.countOfOutputChannels = _currentDevice.get("maxOutputChannels", -1)
        _currentSoundCard.inputLatency = [_currentDevice.get("defaultLowInputLatency", -1),
                                          _currentDevice.get("defaultHighInputLatency", -1)]
        _currentSoundCard.interfaceID = _currentDevice.get("index", -1)
        _currentSoundCard.interfaceName = _currentDevice.get("name", "No name provided.")
        _currentSoundCard.outputLatency = [_currentDevice.get("defaultLowOutputLatency", -1),
                                           _currentDevice.get("defaultHighOutputLatency", -1)]

        # Checks if it is default input / output device
        if (_devices.get_default_input_device_info()).get("index", -1) == _currentSoundCard.interfaceID:
            _currentSoundCard.isDefaultInputInterface = True

        if (_devices.get_default_output_device_info()).get("index", -1) == _currentSoundCard.interfaceID:
            _currentSoundCard.isDefaultOutputInterface = True

        # Saves default accepted sampling rate
        _currentSoundCard.samplingRates = [_currentDevice.get("defaultSampleRate", -1)]

        # Tests other sampling rates and add them if they are valid
        for _sampleRateUnderTest in [48000.0, 96000.0, 192000.0]:
            try:
                if _devices.is_format_supported(rate=_sampleRateUnderTest,
                                                input_channels=_currentSoundCard.countOfInputChannels,
                                                output_channels=_currentSoundCard.countOfOutputChannels,
                                                input_format=_currentDevice.get("structVersion", 2),
                                                output_format=_currentDevice.get("structVersion", 2),
                                                input_device=_currentSoundCard.interfaceID,
                                                output_device=_currentSoundCard.interfaceID):

                    _currentSoundCard.samplingRates.append(_sampleRateUnderTest)
            except ValueError:
                pass

        _soundCards.append(_currentSoundCard)

    return _soundCards


# # Code to test the function
# allCards = getAllSoundCardsInfo()
#
# for n in range(len(allCards)):
#     print allCards[n].interfaceID
#     print allCards[n].interfaceName
#     print allCards[n].isDefaultInputInterface
#     print allCards[n].isDefaultOutputInterface
#     print allCards[n].countOfInputChannels
#     print allCards[n].countOfOutputChannels
#     print allCards[n].samplingRates
#     print allCards[n].bitDepths
#     print allCards[n].inputLatency
#     print allCards[n].outputLatency
#
#     print "--------"
