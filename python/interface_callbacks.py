import strings

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
    :return: Nothing.
    """

    userValues_mlsLength.set(DEFAULT_VALUES_MLS_LENGTH)
    userValues_amplitude.set(DEFAULT_VALUES_AMPLITUDE)
    userValues_predelay.set(DEFAULT_VALUES_PLAYBACK_PREDELAY)
    userValues_decay.set(DEFAULT_VALUES_EXPECTED_DECAY)


def recoverDefaultOutputFilename(saveDataToFile_variable):
    saveDataToFile_variable.set(DEFAULT_VALUES_OUTPUT_FILENAME)


def parseInt(stringNumber):
    try:
        return abs(int(stringNumber))
    except ValueError:
        return strings.TEXT_6


def parseFloat(stringNumber):
    try:
        return abs(float(stringNumber))
    except ValueError:
        return strings.TEXT_6


def validateNumbersCallback(userValues_mlsLength, userValues_amplitude, userValues_predelay, userValues_decay):
    """
    Checks input strings parsing including accepting only positive numbers (returning absolute value in case of
    negative inputs).

    Joe.
    :param userValues_mlsLength:
    :param userValues_amplitude:
    :param userValues_predelay:
    :param userValues_decay:
    :return:
    """

    userValues_mlsLength.set(parseInt(userValues_mlsLength.get()))
    userValues_amplitude.set(parseFloat(userValues_amplitude.get()))
    userValues_predelay.set(parseInt(userValues_predelay.get()))
    userValues_decay.set(parseFloat(userValues_decay.get()))


# TODO: complete this
def testInputDeviceCallback():
    import tkMessageBox
    tkMessageBox.showinfo('Debug ...', 'Complete this part with an input level test ...')


# TODO: make this use the sampling freq and amplitude selected in the window
def testOutputDeviceCallback(deviceToUse, userValues_amplitude):
    import numpy
    import player
    signal1 = [float(userValues_amplitude.get()) * numpy.sin(2 * numpy.pi * 1000 * n/44100) for n in range(44100)]
    signal2 = [float(userValues_amplitude.get()) * numpy.sin(2 * numpy.pi * 2000 * n/44100) for n in range(44100)]

    # Sends them to the sound card
    player.playSignals(signal1, signal2, samplingFreq=44100, normalize=False, deviceIndex=deviceToUse.interfaceID)


def saveDataToFileCallback(saveDataToFile_variable):

    import tkFileDialog
    _filename = tkFileDialog.asksaveasfilename(defaultextension=".wav")

    if _filename != "":
        saveDataToFile_variable.set(_filename)


# TODO: complete this
# TODO: change symbol to receive data from interface (parameters and selected audio i/o)
def startMeasurement(mainWindow, shouldPlot, shouldSaveToFile, shouldSaveToFileFilename):
    # Must:
    # - verify parameters
    # - show "please wait" dialog
    # - call measurement and wait for return data
    # - display a plot and / or save data to file

    if (not shouldPlot) and (not shouldSaveToFile):
        import tkMessageBox
        tkMessageBox.showinfo(strings.TEXT_30, strings.TEXT_32)
        return

    if shouldSaveToFile and not shouldSaveToFileFilename:
        import tkMessageBox
        tkMessageBox.showinfo(strings.TEXT_30, strings.TEXT_31)
    else:
        import interface
        # TODO: this is really dirty, should find another way of doing it
        interface.returnedValue = True
        mainWindow.destroy()
