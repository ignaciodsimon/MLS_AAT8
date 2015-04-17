"""
Callback functions of the graphic interface.

Joe.
"""


from MLS import language_strings
from MLS.logic_layer import player
from MLS.logic_layer import generate_mls

# Constants
DEFAULT_VALUES_MLS_LENGTH = 32768
DEFAULT_VALUES_AMPLITUDE = 0.5
DEFAULT_VALUES_PLAYBACK_PREDELAY = 250
DEFAULT_VALUES_EXPECTED_DECAY = 2.0
DEFAULT_VALUES_OUTPUT_FILENAME = "/Users/maese/Documents/otra.wav"
DEFAULT_VALUES_AVERAGES = 1
DEFAULT_VALUES_SHOULD_SAVE_TO_FILE = False
DEFAULT_VALUES_SHOULD_PLOT = True
DEFAULT_VALUES_DUAL_MODE_ENABLED = False
DEFAULT_VALUES_HW_CORRECTION_L_FILENAME = ""
DEFAULT_VALUES_HW_CORRECTION_R_FILENAME = ""
DEFAULT_VALUES_HW_CORRECTION_ENABLED = False


# Callback functions
def recoverDefaultValuesCallback(userValues_mlsLength, userValues_amplitude, userValues_predelay,
                                 userValues_decay, userValues_averages, userValues__plotOutputDataCheck,
                                 userValues_saveDataToFileCheck, defaultMeasurementSetup, userValues_channelMode,
                                 userValues_hwIRCorrectionEnabledCheck, userValues_hwCorrectionFilename_L,
                                 userValues_hwCorrectionFilename_R):
    """
    Callback function for "Recover default values" button on section 2 "measurement settings".

    Joe.
    """

    if defaultMeasurementSetup is None:
        userValues_mlsLength.set(DEFAULT_VALUES_MLS_LENGTH)
        userValues_amplitude.set(DEFAULT_VALUES_AMPLITUDE)
        userValues_predelay.set(DEFAULT_VALUES_PLAYBACK_PREDELAY)
        userValues_decay.set(DEFAULT_VALUES_EXPECTED_DECAY)
        userValues_averages.set(DEFAULT_VALUES_AVERAGES)
        userValues__plotOutputDataCheck.set(DEFAULT_VALUES_SHOULD_PLOT)
        userValues_saveDataToFileCheck.set(DEFAULT_VALUES_SHOULD_SAVE_TO_FILE)

        if DEFAULT_VALUES_DUAL_MODE_ENABLED:
            userValues_channelMode.set(1)
        else:
            userValues_channelMode.set(0)

        userValues_hwCorrectionFilename_L.set(DEFAULT_VALUES_HW_CORRECTION_L_FILENAME)
        userValues_hwCorrectionFilename_R.set(DEFAULT_VALUES_HW_CORRECTION_R_FILENAME)
        userValues_hwIRCorrectionEnabledCheck.set(DEFAULT_VALUES_HW_CORRECTION_ENABLED)

    else:
        userValues_mlsLength.set(defaultMeasurementSetup.MLSLength)
        userValues_amplitude.set(defaultMeasurementSetup.signalAmplitude)
        userValues_predelay.set(defaultMeasurementSetup.preDelayForPlayback)
        userValues_decay.set(defaultMeasurementSetup.decayTime)
        userValues_averages.set(defaultMeasurementSetup.numberOfPreAverages)
        userValues__plotOutputDataCheck.set(defaultMeasurementSetup.shouldPlot)
        userValues_saveDataToFileCheck.set(defaultMeasurementSetup.shouldSaveToFile)

        if defaultMeasurementSetup.dualChannelMode:
            userValues_channelMode.set(1)
        else:
            userValues_channelMode.set(0)

        userValues_hwIRCorrectionEnabledCheck.set(defaultMeasurementSetup.shouldUseHWCorrection)
        userValues_hwCorrectionFilename_L.set(defaultMeasurementSetup.hwCorrectionFilename_L)
        userValues_hwCorrectionFilename_R.set(defaultMeasurementSetup.hwCorrectionFilename_R)


def recoverDefaultOutputFilename(saveDataToFile_variable, defaultMeasurementSetup):
    """
    Sets the output filename to the default value. Default text is obtained from the strings file.

    Joe.
    :param saveDataToFile_variable: Variable of type StringVar that will hold the string.
    """

    if defaultMeasurementSetup is None:
        saveDataToFile_variable.set(DEFAULT_VALUES_OUTPUT_FILENAME)
    else:
        saveDataToFile_variable.set(defaultMeasurementSetup.shouldSaveToFileFilename)


def parseInt(stringNumber):
    """
    Parses an int to int with absolute value. Return an error string in case it can not be parsed.

    Joe.
    :param stringNumber: String containing an int.
    :return: Parsed integer in absolute value or error string.
    """
    try:
        return abs(int(float(stringNumber)))
    except ValueError:
        return language_strings.TEXT_6


def parseFloat(stringNumber):
    """
    Parses a float to float with absolute value. Return an error string in case it can not be parsed.

    Joe.
    :param stringNumber: String containing a float.
    :return: Parsed float in absolute value or error string.
    """
    try:
        return abs(float(stringNumber))
    except ValueError:
        return language_strings.TEXT_6


def validateNumbersCallback(userValues_mlsLength, userValues_amplitude, userValues_predelay, userValues_decay):
    """
    Checks input strings parsing including accepting only positive numbers (returning absolute value in case of
    negative inputs).

    Joe.
    :param userValues_mlsLength: Variable holding the MLS length, object of type StringVar.
    :param userValues_amplitude: Variable holding the MLS amplitude, object of type StringVar.
    :param userValues_predelay: Variable holding the MLS predelay, object of type StringVar.
    :param userValues_decay: Variable holding the recording decay, object of type StringVar.
    """

    userValues_mlsLength.set(parseInt(userValues_mlsLength.get()))
    userValues_amplitude.set(parseFloat(userValues_amplitude.get()))
    userValues_predelay.set(parseInt(userValues_predelay.get()))
    userValues_decay.set(parseFloat(userValues_decay.get()))


def testInputDeviceCallback():
    """
    Checks input device by measuring the received level.

    Joe.
    """

    # TODO: complete this
    import tkMessageBox
    tkMessageBox.showinfo('Debug ...', 'Complete this part with an input level test ...')


def testOutputDeviceCallback(deviceToUse, userValues_amplitude):
    """
    Sends an MLS signal to the output of the selected device with the given amplitude.

    Joe.
    :param deviceToUse: Output device to use, type SoundCard.
    :param userValues_amplitude: Amplitude of sinus signals, from 0.0 to 1.0.
    """

    # TODO: make this use the sampling freq and amplitude selected in the window
    _MLSSignal = generate_mls.generateMLS(pow(2, 15), float(userValues_amplitude.get()))

    # Sends them to the sound card
    player.playSignals(_MLSSignal, _MLSSignal, samplingFreq=44100, normalize=False, deviceIndex=deviceToUse.interfaceID)


def saveDataToFileCallback(saveDataToFile_variable):

    import tkFileDialog
    _filename = tkFileDialog.asksaveasfilename(defaultextension=".wav")

    if _filename != "":
        saveDataToFile_variable.set(_filename)


def openFileCallback(openFile_variable):

    import tkFileDialog

    _fileOpenOptions = dict(defaultextension='.wav',
                            filetypes=[('WAV files', '*.wav'), ('All files', '*.*')])
    _filename = tkFileDialog.askopenfilename(**_fileOpenOptions)

    if _filename != "":
        openFile_variable.set(_filename)


def startMeasurement(mainWindow, shouldPlot, shouldSaveToFile, shouldSaveToFileFilename, shouldStartMeasurement):
    """
    Closes the window and makes it return the necessary object to start the measurement.

    Joe.
    :param mainWindow: Window object to close.
    :param shouldPlot: Used to check if the user selected at least one output option.
    :param shouldSaveToFile: Used to check if the user selected at least one output option.
    :param shouldSaveToFileFilename: Used to check if user inserted filename.
    """

    # TODO: change symbol to receive data from interface (parameters and selected audio i/o)
    # Must:
    # - verify parameters
    # - show "please wait" dialog
    # - call measurement and wait for return data
    # - display a plot and / or save data to file

    # Checks if user selected at least one output option
    if (not shouldPlot) and (not shouldSaveToFile):
        import tkMessageBox
        tkMessageBox.showinfo(language_strings.TEXT_30, language_strings.TEXT_32)
        return

    # Check if output filename is present when necessary
    if shouldSaveToFile and not shouldSaveToFileFilename:
        import tkMessageBox
        tkMessageBox.showinfo(language_strings.TEXT_30, language_strings.TEXT_31)
    else:
        # from MLS.interface_layer import interface
        shouldStartMeasurement.set(True)
        mainWindow.destroy()


def changedInputDeviceCallBack(newValue, inputAudioInterfaces, inputDeviceLabelText, *args):
    """
    Callback from option list of input devices. Used to update the shown text with details of the interface.

    Joe.
    :param newValue: New text that should display.
    :param inputAudioInterfaces: List of available input interfaces.
    :param inputDeviceLabelText: Associated variable that updates the options list.
    :param args: Non used parameter, coming from lambda expression.
    """

    # Finds which device was selected by its name
    for _card in inputAudioInterfaces:
        if _card.interfaceName == newValue:
            global selectedInputInterface
            selectedInputInterface = _card

    # Sets the new description
    inputDeviceLabelText.set(language_strings.TEXT_24 + "\n  " + str(selectedInputInterface.samplingRates) + "\n" +
                             language_strings.TEXT_25 + "\n  " + str(selectedInputInterface.bitDepths) + "\n" +
                             language_strings.TEXT_26 + "\n  " + str(selectedInputInterface.countOfInputChannels) + "\n" +
                             language_strings.TEXT_27 + "\n  " + str(selectedInputInterface.countOfOutputChannels) + "\n" +
                             language_strings.TEXT_28 + "\n  " + str("%.2f" % (selectedInputInterface.inputLatency[0]*1000))
                             + " - " + str("%.2f" % (selectedInputInterface.inputLatency[1]*1000)))


def changedOutputDeviceCallBack(newValue, outputAudioInterfaces, outputDeviceLabelText, *args):
    """
    Callback from option list of output devices. Used to update the shown text with details of the interface.

    Joe.
    :param newValue: New text that should display.
    :param outputAudioInterfaces: List of available output interfaces.
    :param outputDeviceLabelText: Associated variable that updates the options list.
    :param args: Non used parameter, coming from lambda expression.
    """

    # Finds which device was selected by its name
    for _card in outputAudioInterfaces:
        if _card.interfaceName == newValue:
            global selectedOutputInterface
            selectedOutputInterface = _card

    # Sets the new description
    outputDeviceLabelText.set(language_strings.TEXT_24 + "\n  " + str(selectedOutputInterface.samplingRates) + "\n" +
                              language_strings.TEXT_25 + "\n  " + str(selectedOutputInterface.bitDepths) + "\n" +
                              language_strings.TEXT_26 + "\n  " + str(selectedOutputInterface.countOfInputChannels) + "\n" +
                              language_strings.TEXT_27 + "\n  " + str(selectedOutputInterface.countOfOutputChannels) + "\n" +
                              language_strings.TEXT_29 + "\n  " + str("%.2f" % (selectedOutputInterface.outputLatency[0]*1000))
                              + " - " + str("%.2f" % (selectedOutputInterface.outputLatency[1]*1000)))
