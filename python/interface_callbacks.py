
# Constants
DEFAULT_VALUES_MLS_LENGTH = 32768
DEFAULT_VALUES_AMPLITUDE = 0.5
DEFAULT_VALUES_PLAYBACK_PREDELAY = 250
DEFAULT_VALUES_EXPECTED_DECAY = 5.0
DEFAULT_VALUES_OUTPUT_FILENAME = "outputFile.txt"


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
        return "Invalid"


def parseFloat(stringNumber):
    try:
        return abs(float(stringNumber))
    except ValueError:
        return "Invalid"


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


# TODO: complete this
def testOutputDeviceCallback():
    import tkMessageBox
    tkMessageBox.showinfo('Debug ...', 'Complete this part with an output signal test ...')


# TODO: complete this
def saveDataToFileCallback(saveDataToFile_variable):

    import tkFileDialog
    _filename = tkFileDialog.asksaveasfilename(defaultextension=".txt")

    if _filename != "":
        print "Selected to save as: ", _filename
        saveDataToFile_variable.set(_filename)
    else:
        print "No file selected ..."
    # tkMessageBox.showinfo('Debug ...', 'Complete this part with a save dialog ...')


# TODO: complete this
# TODO: change symbol to receive data from interface (parameters and selected audio i/o)
def startMeasurement(mainWindow):
    # Must:
    # - verify parameters
    # - show "please wait" dialog
    # - call measurement and wait for return data
    # - display a plot and / or save data to file

    import interface

    # TODO: this is really dirty, should find another way of doing it
    interface.returnedValue = True
    mainWindow.destroy()
