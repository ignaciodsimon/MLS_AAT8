class MeasurementSettings:
    """
    Measurement settings definition class. Used to provide information of measurement to be performed.

    Public fields:

    MLSLength: Desired length of MLS signal.
    inputDeviceSamplFreq: Input device sampling frequency.
    outputDeviceSamplFreq: Output device sampling frequency.
    signalAmplitude: Amplitude of MLS signal.
    preDelayForPlayback: Pre-delay to correct for the latency of sound card.
    decayTime: Decay time of system-under-test. Should be a bit larger than expected one.
    inputDevice: Input audio device to use, index from zero. Omit to use default device.
    outputDevice: Output audio device to use, index from zero. Omit to use default device.

    Joe.
    """

    # Class constructor
    def __init__(self):
        self.data = []

    # Public fields
    MLSLength = 32768
    inputDeviceSamplFreq = 44100
    outputDeviceSamplFreq = 44100
    signalAmplitude = 0.5
    preDelayForPlayback = 0.25
    decayTime = 5.0
    inputDevice = -1
    outputDevice = -1
    normalizeOutput = 1
    referenceSignalIsLeft = False

    shouldPlot = False
    shouldSaveToFile = False
    shouldSaveToFileFilename = ""

    numberOfAverages = 1


class MeasurementResult:
    """
    Measurement results definition class. Used to return information of performed measurement.

    Joe.
    """

    # Class constructor
    def __init__(self):
        self.data = []

    # Public fields
    settings = 0
    computedImpulseResponse = 0
    partialIR_Left = 0
    partialIR_Right = 0


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
