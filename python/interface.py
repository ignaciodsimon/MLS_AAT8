

# Internal imports
import interface_callbacks
import strings
import soundcards
import measurement


# Global constants
BACKGROUND_COLOR = "#10547F"
# BACKGROUND_COLOR = "#00446f"
FOREGROUND_COLOR = "#FFFFFF"
TOP_BANNER_FILENAME = "top_banner.gif"
WINDOW_SIZE = "910x570"

# Text strings
WINDOW_TITLE = "Impulse response measuring system - AAU 2015"

# Global variables
inputAudioInterfaces = []
outputAudioInterfaces = []
selectedInputInterface = None
selectedOutputInterface = None

inputDeviceLabelText = None
outputDeviceLabelText = None

returnedValue = False

def fillComboWithList(optionStrings, inputCombo, associatedVar, defaultIndex):

    import Tkinter

    # Cleans combo options
    inputCombo['menu'].delete(0, 'end')

    # Sets default option
    associatedVar.set(optionStrings[defaultIndex])

    # Fill all options
    for choice in optionStrings:
        inputCombo['menu'].add_command(label=choice, command=Tkinter._setit(associatedVar, choice))


def loadDeviceLists(inputDeviceCombo, inputDevicesVar, outputDeviceCombo, outputDevicesVar):

    _availableCards = soundcards.getAllSoundCardsInfo()

    _inputCardsNames = []
    _outputCardsNames = []
    _defaultInputCard = 0
    _defaultOutputCard = 0
    for _currentCard in _availableCards:

        # If it has inputs
        if _currentCard.countOfInputChannels > 0:
            inputAudioInterfaces.append(_currentCard)
            _inputCardsNames.append(_currentCard.interfaceName)

        # If it has outputs
        if _currentCard.countOfOutputChannels > 0:
            outputAudioInterfaces.append(_currentCard)
            _outputCardsNames.append(_currentCard.interfaceName)

        # If it is the default input device
        if _currentCard.isDefaultInputInterface:
            global selectedInputInterface
            selectedInputInterface = _currentCard
            _defaultInputCard = len(_inputCardsNames)-1

        # If it its the default output device
        if _currentCard.isDefaultOutputInterface:
            global selectedOutputInterface
            selectedOutputInterface = _currentCard
            _defaultOutputCard = len(_outputCardsNames)-1

    # Loads input devices combo and wires callback
    fillComboWithList(_inputCardsNames, inputDeviceCombo, inputDevicesVar, _defaultInputCard)
    inputDevicesVar.trace("w", lambda *args: changedInputDeviceCallBack(inputDevicesVar.get(), *args))

    # Loads output devices combo and wires callback
    fillComboWithList(_outputCardsNames, outputDeviceCombo, outputDevicesVar, _defaultOutputCard)
    outputDevicesVar.trace("w", lambda *args: changedOutputDeviceCallBack(outputDevicesVar.get(), *args))

    # Calls callback to update information
    changedInputDeviceCallBack(inputDevicesVar.get(), None)
    changedOutputDeviceCallBack(outputDevicesVar.get(), None)

def changedInputDeviceCallBack(newValue, *args):
    for _card in inputAudioInterfaces:
        if _card.interfaceName == newValue:
            global selectedInputInterface
            selectedInputInterface = _card

    inputDeviceLabelText.set(strings.TEXT_24 + "\n  " + str(selectedInputInterface.samplingRates) + "\n" +
                             strings.TEXT_25 + "\n  " + str(selectedInputInterface.bitDepths) + "\n" +
                             strings.TEXT_26 + "\n  " + str(selectedInputInterface.countOfInputChannels) + "\n" +
                             strings.TEXT_27 + "\n  " + str(selectedInputInterface.countOfOutputChannels) + "\n" +
                             strings.TEXT_28 + "\n  " + str("%.2f" % (selectedInputInterface.inputLatency[0]*1000))
                             + " - " + str("%.2f" % (selectedInputInterface.inputLatency[1]*1000)))


def changedOutputDeviceCallBack(newValue, *args):
    for _card in outputAudioInterfaces:
        if _card.interfaceName == newValue:
            global selectedOutputInterface
            selectedOutputInterface = _card

    outputDeviceLabelText.set(strings.TEXT_24 + "\n  " + str(selectedOutputInterface.samplingRates) + "\n" +
                              strings.TEXT_25 + "\n  " + str(selectedOutputInterface.bitDepths) + "\n" +
                              strings.TEXT_26 + "\n  " + str(selectedOutputInterface.countOfInputChannels) + "\n" +
                              strings.TEXT_27 + "\n  " + str(selectedOutputInterface.countOfOutputChannels) + "\n" +
                              strings.TEXT_29 + "\n  " + str("%.2f" % (selectedOutputInterface.outputLatency[0]*1000))
                              + " - " + str("%.2f" % (selectedOutputInterface.outputLatency[1]*1000)))


def buildInterface():

    import Tkinter

    # Root window
    root = Tkinter.Tk()
    root.title(WINDOW_TITLE)
    root.resizable(width=False, height=False)
    root.geometry(WINDOW_SIZE)
    root.configure(padx=0, pady=0, background=BACKGROUND_COLOR)

    logo = Tkinter.PhotoImage(file=TOP_BANNER_FILENAME)
    w1 = Tkinter.Label(root, image=logo)
    w1.configure(background=BACKGROUND_COLOR, padx=0, pady=0)
    w1.place(x=0, y=0)

    # -----------------------------
    #  Frame 1 - Hardware settings
    # -----------------------------
    hardwareSettingFrame = Tkinter.LabelFrame(root,
                                              text=strings.TEXT_1,
                                              width=580,
                                              height=300)
    hardwareSettingFrame.configure(background=BACKGROUND_COLOR)
    hardwareSettingFrame.place(x=10, y=90)
    hardwareSettingFrame.configure(font=('', 0, 'bold'), foreground=FOREGROUND_COLOR)

    # Input / output devices labels
    hdwInputLabel = Tkinter.Label(hardwareSettingFrame, text=strings.TEXT_2)
    hdwInputLabel.place(x=20, y=10, anchor="nw")
    hdwInputLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    hdwOutputLabel = Tkinter.Label(hardwareSettingFrame, text=strings.TEXT_3)
    hdwOutputLabel.place(x=300, y=10, anchor="nw")
    hdwOutputLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

    # Input / output devices combos
    inputDevicesVar = Tkinter.StringVar(hardwareSettingFrame)
#    inputDevicesList.set(strings.TEXT_4)
    inputDeviceCombo = Tkinter.OptionMenu(hardwareSettingFrame, inputDevicesVar, strings.TEXT_4)
    inputDeviceCombo.config(width=24, background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    inputDeviceCombo.place(x=20, y=30)

    outputDevicesVar = Tkinter.StringVar(hardwareSettingFrame)
#    outputDevicesList.set(strings.TEXT_4)
    outputDeviceCombo = Tkinter.OptionMenu(hardwareSettingFrame, outputDevicesVar, strings.TEXT_4)
    outputDeviceCombo.config(width=24, background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    outputDeviceCombo.place(x=300, y=30)

    # Test buttons
    testInputDeviceButton = Tkinter.Button(hardwareSettingFrame,
                                           text=strings.TEXT_5, width=2,
                                           command=lambda: interface_callbacks.testInputDeviceCallback())
    testInputDeviceButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    testInputDeviceButton.place(x=230, y=30)

    testOutputDeviceButton = Tkinter.Button(hardwareSettingFrame,
                                            text=strings.TEXT_5, width=2,
                                            command=lambda: interface_callbacks.testOutputDeviceCallback())
    testOutputDeviceButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    testOutputDeviceButton.place(x=510, y=30)

    # Input /output devices properties labels
    global inputDeviceLabelText
    inputDeviceLabelText = Tkinter.StringVar(hardwareSettingFrame)
    inputDeviceLabel = Tkinter.Label(hardwareSettingFrame,
                                     text="", textvariable=inputDeviceLabelText,
                                     justify=Tkinter.LEFT)
    inputDeviceLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    inputDeviceLabel.place(x=20, y=70)

    global outputDeviceLabelText
    outputDeviceLabelText = Tkinter.StringVar(hardwareSettingFrame)
    outputDeviceLabel = Tkinter.Label(hardwareSettingFrame,
                                     text="", textvariable=outputDeviceLabelText,
                                     justify=Tkinter.LEFT)
    outputDeviceLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    outputDeviceLabel.place(x=300, y=70)

    # --------------------------------
    #  Frame 2 - Measurement settings
    # --------------------------------
    measurementSettingFrame = Tkinter.LabelFrame(root,
                                                 text=strings.TEXT_7,
                                                 width=300,
                                                 height=300)
    measurementSettingFrame.place(x=600, y=90)
    measurementSettingFrame.configure(font=('', 0, 'bold'), background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

    # Labels
    generatedSignalTitleLabel = Tkinter.Label(measurementSettingFrame, text=strings.TEXT_8,
                                              justify=Tkinter.LEFT)
    generatedSignalTitleLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    generatedSignalTitleLabel.place(x=20, y=10)

    generatedSignalMLSLengthLabel = Tkinter.Label(measurementSettingFrame, text=strings.TEXT_9,
                                                  justify=Tkinter.LEFT)
    generatedSignalMLSLengthLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    generatedSignalMLSLengthLabel.place(x=30, y=40)

    generatedSignalAmplitudeLabel = Tkinter.Label(measurementSettingFrame, text=strings.TEXT_10,
                                                  justify=Tkinter.LEFT)
    generatedSignalAmplitudeLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    generatedSignalAmplitudeLabel.place(x=30, y=70)

    generatedSignalPlaybackDelayLabel = Tkinter.Label(measurementSettingFrame, text=strings.TEXT_11,
                                                      justify=Tkinter.LEFT)
    generatedSignalPlaybackDelayLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    generatedSignalPlaybackDelayLabel.place(x=30, y=100)

    recordedSignalTitleLabel = Tkinter.Label(measurementSettingFrame, text=strings.TEXT_12,
                                             justify=Tkinter.LEFT)
    recordedSignalTitleLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    recordedSignalTitleLabel.place(x=20, y=150)

    recordedSignalDelayLabel = Tkinter.Label(measurementSettingFrame, text=strings.TEXT_13,
                                             justify=Tkinter.LEFT)
    recordedSignalDelayLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    recordedSignalDelayLabel.place(x=30, y=180)

    # Inputs
    userValues_mlsLength = Tkinter.StringVar()
    mlsLengthInputEntry = Tkinter.Entry(measurementSettingFrame, width=8,
                                        textvariable=userValues_mlsLength, justify=Tkinter.RIGHT)
    mlsLengthInputEntry.config(highlightbackground=BACKGROUND_COLOR, background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    mlsLengthInputEntry.place(x=200, y=40)

    userValues_amplitude = Tkinter.StringVar()
    amplitudeInputEntry = Tkinter.Entry(measurementSettingFrame, width=8,
                                        textvariable=userValues_amplitude, justify=Tkinter.RIGHT)
    amplitudeInputEntry.config(highlightbackground=BACKGROUND_COLOR, background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    amplitudeInputEntry.place(x=200, y=70)

    userValues_predelay = Tkinter.StringVar()
    predelayInputEntry = Tkinter.Entry(measurementSettingFrame, width=8,
                                       textvariable=userValues_predelay, justify=Tkinter.RIGHT)
    predelayInputEntry.config(highlightbackground=BACKGROUND_COLOR, background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    predelayInputEntry.place(x=200, y=100)

    userValues_decay = Tkinter.StringVar()
    decayInputEntry = Tkinter.Entry(measurementSettingFrame, width=8,
                                    textvariable=userValues_decay, justify=Tkinter.RIGHT)
    decayInputEntry.config(highlightbackground=BACKGROUND_COLOR, background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    decayInputEntry.place(x=200, y=180)

    measurementSettingsRecoverDefaultValuesButton = Tkinter.Button(measurementSettingFrame, text=strings.TEXT_14,
                                                                   command=lambda: interface_callbacks.
                                                                   recoverDefaultValuesCallback(userValues_mlsLength,
                                                                                                userValues_amplitude,
                                                                                                userValues_predelay,
                                                                                                userValues_decay))
    measurementSettingsRecoverDefaultValuesButton.config(highlightbackground=BACKGROUND_COLOR,
                                                         bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    measurementSettingsRecoverDefaultValuesButton.place(x=20, y=230)

    measurementSettingsValidateNumbersButton = Tkinter.Button(measurementSettingFrame,
                                                              text=strings.TEXT_15,
                                                              command=lambda: interface_callbacks.
                                                              validateNumbersCallback(userValues_mlsLength,
                                                                                      userValues_amplitude,
                                                                                      userValues_predelay,
                                                                                      userValues_decay))
    measurementSettingsValidateNumbersButton.config(highlightbackground=BACKGROUND_COLOR,
                                                    bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    measurementSettingsValidateNumbersButton.place(x=150, y=230)

    # -----------------------
    #  Frame 3 - Output data
    # -----------------------
    outputDataFrame = Tkinter.LabelFrame(root,
                                         text=strings.TEXT_16,
                                         width=450,
                                         height=135)
    outputDataFrame.place(x=10, y=395)
    outputDataFrame.configure(font=('', 0, 'bold'), background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

    # Save to file options
    saveDataToFileCheck = Tkinter.IntVar()
    saveDataToFileCheck.set(False)

    saveDataToFileCheckButton = Tkinter.Checkbutton(outputDataFrame, text="", variable=saveDataToFileCheck)
    saveDataToFileCheckButton.configure(background=BACKGROUND_COLOR)
    saveDataToFileCheckButton.place(x=10, y=10)

    saveDataToFileLabel = Tkinter.Label(outputDataFrame, text=strings.TEXT_17)
    saveDataToFileLabel.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    saveDataToFileLabel.place(x=35, y=10)

    saveDataToFile_variable = Tkinter.StringVar()
    interface_callbacks.recoverDefaultOutputFilename(saveDataToFile_variable)
    saveDataToFileEntry = Tkinter.Entry(outputDataFrame, textvariable=saveDataToFile_variable, width=40)
    saveDataToFileEntry.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
    saveDataToFileEntry.place(x=35, y=40)

    saveDataToFileButton = Tkinter.Button(outputDataFrame,
                                          width=2, text=strings.TEXT_18,
                                          command=lambda: interface_callbacks.
                                          saveDataToFileCallback(saveDataToFile_variable))
    saveDataToFileButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    saveDataToFileButton.place(x=380, y=40)

    # Plot output data options
    plotOutputDataCheck = Tkinter.IntVar()
    plotOutputDataCheck.set(True)

    plotOutputDataCheckButton = Tkinter.Checkbutton(outputDataFrame, text="", variable=plotOutputDataCheck)
    plotOutputDataCheckButton.configure(background=BACKGROUND_COLOR)
    plotOutputDataCheckButton.place(x=10, y=80)

    plotOutputDataLabel = Tkinter.Label(outputDataFrame, text=strings.TEXT_19)
    plotOutputDataLabel.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    plotOutputDataLabel.place(x=35, y=80)

    # -----------------------
    #  Frame 4 - Output data
    # -----------------------
    executeMeasurementFrame = Tkinter.LabelFrame(root,
                                                 text=strings.TEXT_20,
                                                 width=430,
                                                 height=135)
    executeMeasurementFrame.place(x=470, y=395)
    executeMeasurementFrame.configure(font=('', 0, 'bold'), background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

    executeMeasurementButton = Tkinter.Button(executeMeasurementFrame, text=strings.TEXT_21,
                                              command=lambda: interface_callbacks.startMeasurement(root))
    executeMeasurementButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    executeMeasurementButton.place(x=40, y=20)

    executeMeasurementLabel = Tkinter.Label(executeMeasurementFrame, text=strings.TEXT_22)
    executeMeasurementLabel.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    executeMeasurementLabel.place(x=40, y=60)

    status = Tkinter.Label(root, text=strings.TEXT_23,
                           bd=1, relief=Tkinter.SUNKEN, anchor=Tkinter.W)
    status.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)

    # ---------------------------
    #  Loads data into interface
    # ---------------------------

    # Sets default values
    interface_callbacks.recoverDefaultValuesCallback(userValues_mlsLength, userValues_amplitude,
                                                     userValues_predelay, userValues_decay)

    # Loads combos
    loadDeviceLists(inputDeviceCombo, inputDevicesVar, outputDeviceCombo, outputDevicesVar)

    # Gives control to window manager
    root.mainloop()

    if returnedValue == True:
        measurementSettings = measurement.MeasurementSettings()

        measurementSettings.MLSLength = int(userValues_mlsLength.get())
        measurementSettings.inputDeviceSamplFreq = selectedInputInterface.samplingRates[0]
        measurementSettings.outputDeviceSamplFreq = selectedOutputInterface.samplingRates[0]
        measurementSettings.signalAmplitude = float(userValues_amplitude.get())
        measurementSettings.preDelayForPlayback = float(userValues_predelay.get()) / 1000.0
        measurementSettings.decayTime = float(userValues_decay.get())
        measurementSettings.inputDevice = selectedInputInterface.interfaceID
        measurementSettings.outputDevice = selectedOutputInterface.interfaceID

        measurementSettings.shouldPlot = plotOutputDataCheck.get()
        measurementSettings.shouldSaveToFile = saveDataToFileCheck.get()
        measurementSettings.shouldSaveToFileFilename = saveDataToFile_variable.get()

        return measurementSettings
    else:
        return False
