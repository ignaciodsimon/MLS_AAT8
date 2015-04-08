"""
Callback functions of the graphic interface.
"""


import strings
import numpy
import player
import generateMLS

# Constants
DEFAULT_VALUES_MLS_LENGTH = 32768
DEFAULT_VALUES_AMPLITUDE = 0.5
DEFAULT_VALUES_PLAYBACK_PREDELAY = 250
DEFAULT_VALUES_EXPECTED_DECAY = 5.0
DEFAULT_VALUES_OUTPUT_FILENAME = ""


# Callback functions
def recoverDefaultValuesCallback(userValues_mlsLength, userValues_amplitude, userValues_predelay, userValues_decay):
    """
    Callback function for "Recover default values" button on section 2 "measurement settings".

    Joe.
    """

    userValues_mlsLength.set(DEFAULT_VALUES_MLS_LENGTH)
    userValues_amplitude.set(DEFAULT_VALUES_AMPLITUDE)
    userValues_predelay.set(DEFAULT_VALUES_PLAYBACK_PREDELAY)
    userValues_decay.set(DEFAULT_VALUES_EXPECTED_DECAY)


def recoverDefaultOutputFilename(saveDataToFile_variable):
    """
    Sets the output filename to the default value. Default text is obtained from the strings file.

    :param saveDataToFile_variable: Variable of type StringVar that will hold the string.
    """
    saveDataToFile_variable.set(DEFAULT_VALUES_OUTPUT_FILENAME)


def parseInt(stringNumber):
    """
    Parses an int to int with absolute value. Return an error string in case it can not be parsed.

    :param stringNumber: String containing an int.
    :return: Parsed integer in absolute value or error string.
    """
    try:
        return abs(int(stringNumber))
    except ValueError:
        return strings.TEXT_6


def parseFloat(stringNumber):
    """
    Parses a float to float with absolute value. Return an error string in case it can not be parsed.

    :param stringNumber: String containing a float.
    :return: Parsed float in absolute value or error string.
    """
    try:
        return abs(float(stringNumber))
    except ValueError:
        return strings.TEXT_6


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
    """

    # TODO: complete this
    import tkMessageBox
    tkMessageBox.showinfo('Debug ...', 'Complete this part with an input level test ...')


def testOutputDeviceCallback(deviceToUse, userValues_amplitude):
    """
    Sends an MLS signal to the output of the selected device with the given amplitude.

    :param deviceToUse: Output device to use, type SoundCard.
    :param userValues_amplitude: Amplitude of sinus signals, from 0.0 to 1.0.
    """

    # TODO: make this use the sampling freq and amplitude selected in the window
    _MLSSignal = generateMLS.generateMLS(pow(2, 15), float(userValues_amplitude.get()))

    # Sends them to the sound card
    player.playSignals(_MLSSignal, _MLSSignal, samplingFreq=44100, normalize=False, deviceIndex=deviceToUse.interfaceID)


def saveDataToFileCallback(saveDataToFile_variable):

    import tkFileDialog
    _filename = tkFileDialog.asksaveasfilename(defaultextension=".wav")

    if _filename != "":
        saveDataToFile_variable.set(_filename)


def startMeasurement(mainWindow, shouldPlot, shouldSaveToFile, shouldSaveToFileFilename):
    """
    Closes the window and makes it return the necessary object to start the measurement.

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
        tkMessageBox.showinfo(strings.TEXT_30, strings.TEXT_32)
        return

    # Check if output filename is present when necessary
    if shouldSaveToFile and not shouldSaveToFileFilename:
        import tkMessageBox
        tkMessageBox.showinfo(strings.TEXT_30, strings.TEXT_31)
    else:
        import interface
        # TODO: this is really dirty, should find another way of doing it
        interface.returnedValue = True
        mainWindow.destroy()


def changedInputDeviceCallBack(newValue, inputAudioInterfaces, inputDeviceLabelText, *args):
    """
    Callback from option list of input devices. Used to update the shown text with details of the interface.

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
    inputDeviceLabelText.set(strings.TEXT_24 + "\n  " + str(selectedInputInterface.samplingRates) + "\n" +
                             strings.TEXT_25 + "\n  " + str(selectedInputInterface.bitDepths) + "\n" +
                             strings.TEXT_26 + "\n  " + str(selectedInputInterface.countOfInputChannels) + "\n" +
                             strings.TEXT_27 + "\n  " + str(selectedInputInterface.countOfOutputChannels) + "\n" +
                             strings.TEXT_28 + "\n  " + str("%.2f" % (selectedInputInterface.inputLatency[0]*1000))
                             + " - " + str("%.2f" % (selectedInputInterface.inputLatency[1]*1000)))


def changedOutputDeviceCallBack(newValue, outputAudioInterfaces, outputDeviceLabelText, *args):
    """
    Callback from option list of output devices. Used to update the shown text with details of the interface.

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
    outputDeviceLabelText.set(strings.TEXT_24 + "\n  " + str(selectedOutputInterface.samplingRates) + "\n" +
                              strings.TEXT_25 + "\n  " + str(selectedOutputInterface.bitDepths) + "\n" +
                              strings.TEXT_26 + "\n  " + str(selectedOutputInterface.countOfInputChannels) + "\n" +
                              strings.TEXT_27 + "\n  " + str(selectedOutputInterface.countOfOutputChannels) + "\n" +
                              strings.TEXT_29 + "\n  " + str("%.2f" % (selectedOutputInterface.outputLatency[0]*1000))
                              + " - " + str("%.2f" % (selectedOutputInterface.outputLatency[1]*1000)))
