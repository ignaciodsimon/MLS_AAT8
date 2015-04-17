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

    shouldPlot = False
    shouldSaveToFile = False
    shouldSaveToFileFilename = ""

    numberOfPreAverages = 1
    numberOfPostAverages = 1

    # Used only in single channel mode
    referenceSignalIsLeft = False

    # If enabled, the two inputs are taken as signals
    # If disabled, one input is in loop and used as correction
    dualChannelMode = False

    # In single channel mode, only the Left calibration may be needed
    calibration_Left = None
    calibration_Right = None

    # Only used for dual channel mode, to compensate for HW delay
    hwCorrection_Left = None
    hwCorrection_Right = None

    shouldUseHWCorrection = False
    hwCorrectionFilename_L = ""
    hwCorrectionFilename_R = ""


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

    rawIR_Left = 0
    rawIR_Right = 0

    outputIR_Left = 0
    outputIR_Right = 0

    # computedImpulseResponse = 0
    # partialIR_Left = 0
    # partialIR_Right = 0


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


class ImpulseResponse:
    """
    Impulse response definition class. Used to share impulse responses with associated metadata.

    Joe.
    """

    # Class constructor
    def __init__(self, impulseResponseVector=None):
        self.data = []
        self.impulseResponse = impulseResponseVector
        if impulseResponseVector is not None:
            self.lengthSamples = len(impulseResponseVector)

    impulseResponse = None
    samplingFrequency = 44100
    bitDepth = 16
    lengthSamples = -1
