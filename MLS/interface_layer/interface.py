"""
Functions to create the graphic interface, wire the events and load data.

Function: (will keep the control until the window is closed)
    buildInterface()

Joe.
"""


# Python imports
import os
import sys

# Internal imports
from MLS.interface_layer import interface_callbacks
from MLS import language_strings
from MLS.logic_layer import soundcards
from MLS.type_classes import type_classes

# Global constants
BACKGROUND_COLOR = "#10547F"
FOREGROUND_COLOR = "#FFFFFF"
TOP_BANNER_FILENAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) \
                      + "/top_banner.gif"
WINDOW_SIZE = "1220x570"

# Text strings
WINDOW_TITLE = "Impulse response measuring system - AAU 2015"

# Global variables
inputAudioInterfaces = []
outputAudioInterfaces = []
selectedInputInterface = None
selectedOutputInterface = None
inputDeviceLabelText = None
outputDeviceLabelText = None


def _fillComboWithList(optionStrings, inputCombo, associatedVar, defaultIndex):
    # TODO: comment this
    """

    Joe.
    """

    import Tkinter

    # Cleans combo options
    inputCombo['menu'].delete(0, 'end')

    # Sets default option
    associatedVar.set(optionStrings[defaultIndex])

    # Fill all options
    for choice in optionStrings:
        inputCombo['menu'].add_command(label=choice, command=Tkinter._setit(associatedVar, choice))


def _loadDeviceLists(inputDeviceCombo, inputDevicesVar, outputDeviceCombo, outputDevicesVar):
    # TODO: comment this
    """

    Joe.
    """

    try:
        _availableCards = soundcards.getAllSoundCardsInfo()
    except Exception as ex:
        print "ERROR: could not retrieve the soundcard(s) info! Message: ", ex
        sys.exit()

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
    _fillComboWithList(_inputCardsNames, inputDeviceCombo, inputDevicesVar, _defaultInputCard)
    inputDevicesVar.trace("w", lambda *args: interface_callbacks.
                          changedInputDeviceCallBack(inputDevicesVar.get(), inputAudioInterfaces,
                                                     inputDeviceLabelText, *args))

    # Loads output devices combo and wires callback
    _fillComboWithList(_outputCardsNames, outputDeviceCombo, outputDevicesVar, _defaultOutputCard)
    outputDevicesVar.trace("w", lambda *args: interface_callbacks.
                           changedOutputDeviceCallBack(outputDevicesVar.get(), outputAudioInterfaces,
                                                       outputDeviceLabelText, *args))

    # Calls callback to update information
    interface_callbacks.changedInputDeviceCallBack(inputDevicesVar.get(), inputAudioInterfaces,
                                                   inputDeviceLabelText, None)
    interface_callbacks.changedOutputDeviceCallBack(outputDevicesVar.get(), outputAudioInterfaces,
                                                    outputDeviceLabelText, None)


def setChildWidgetsEnabled(parentWidget, enabled=True):
    """
    Sets the enabled property of all children widgets.

    :param parentWidget: Widget whose children shall be changed!
    :param enabled: True / False, Enable /Disable
    """

    for child in parentWidget.winfo_children():
        if enabled:
            child.configure(state="normal")
        else:
            child.configure(state="disabled")


def buildInterface(defaultMeasurementSetup=None):
    """
    Builds the graphical interface, shows the main window up, loads data from logic layer into
    components and wires the events.

    Joe.

    :param defaultMeasurementSetup: Object <MeasurementSetting> with new settings to override default ones.
    :return: Object of type <Boolean> or <MeasurementSettings>, depending on if a measurement should
    be performed or not.
    """

    import Tkinter

    # Root window
    _root = Tkinter.Tk()
    _root.title(WINDOW_TITLE)
    _root.resizable(width=False, height=False)
    _root.geometry(WINDOW_SIZE)
    _root.configure(padx=0, pady=0, background=BACKGROUND_COLOR)

    _logo = Tkinter.PhotoImage(file=TOP_BANNER_FILENAME)
    _topLogoLabel = Tkinter.Label(_root, image=_logo)
    _topLogoLabel.configure(background=BACKGROUND_COLOR, padx=0, pady=0)
    _topLogoLabel.place(x=0, y=0)

    # -----------------------------
    #  Frame 1 - Hardware settings
    # -----------------------------

    _hardwareSettingFrame = Tkinter.LabelFrame(_root,
                                              text=language_strings.TEXT_1,
                                              width=580,
                                              height=300)
    _hardwareSettingFrame.configure(background=BACKGROUND_COLOR)
    _hardwareSettingFrame.place(x=10, y=90)
    _hardwareSettingFrame.configure(font=('', 0, 'bold'), foreground=FOREGROUND_COLOR)

    # Input / output devices labels
    _hdwInputLabel = Tkinter.Label(_hardwareSettingFrame, text=language_strings.TEXT_2)
    _hdwInputLabel.place(x=20, y=10, anchor="nw")
    _hdwInputLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _hdwOutputLabel = Tkinter.Label(_hardwareSettingFrame, text=language_strings.TEXT_3)
    _hdwOutputLabel.place(x=300, y=10, anchor="nw")
    _hdwOutputLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

    # Input / output devices combos
    _inputDevicesVar = Tkinter.StringVar(_hardwareSettingFrame)
    _inputDeviceCombo = Tkinter.OptionMenu(_hardwareSettingFrame, _inputDevicesVar, language_strings.TEXT_4)
    _inputDeviceCombo.config(width=24, background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _inputDeviceCombo.place(x=20, y=30)

    _outputDevicesVar = Tkinter.StringVar(_hardwareSettingFrame)
    _outputDeviceCombo = Tkinter.OptionMenu(_hardwareSettingFrame, _outputDevicesVar, language_strings.TEXT_4)
    _outputDeviceCombo.config(width=24, background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _outputDeviceCombo.place(x=300, y=30)

    # Test device buttons
    _testInputDeviceButton = Tkinter.Button(_hardwareSettingFrame,
                                           text=language_strings.TEXT_5, width=2,
                                           command=lambda: interface_callbacks.testInputDeviceCallback())
    _testInputDeviceButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    _testInputDeviceButton.place(x=230, y=30)

    _testOutputDeviceButton = Tkinter.Button(_hardwareSettingFrame,
                                            text=language_strings.TEXT_5, width=2,
                                            command=lambda: interface_callbacks.
                                            testOutputDeviceCallback(selectedOutputInterface, _userValues_amplitude))
    _testOutputDeviceButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    _testOutputDeviceButton.place(x=510, y=30)

    # Input /output devices properties labels
    global inputDeviceLabelText
    inputDeviceLabelText = Tkinter.StringVar(_hardwareSettingFrame)
    _inputDeviceLabel = Tkinter.Label(_hardwareSettingFrame,
                                     text="", textvariable=inputDeviceLabelText,
                                     justify=Tkinter.LEFT)
    _inputDeviceLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _inputDeviceLabel.place(x=20, y=70)

    global outputDeviceLabelText
    outputDeviceLabelText = Tkinter.StringVar(_hardwareSettingFrame)
    _outputDeviceLabel = Tkinter.Label(_hardwareSettingFrame,
                                     text="", textvariable=outputDeviceLabelText,
                                     justify=Tkinter.LEFT)
    _outputDeviceLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _outputDeviceLabel.place(x=300, y=70)

    # --------------------------------
    #  Frame 2 - Measurement settings
    # --------------------------------

    _measurementSettingFrame = Tkinter.LabelFrame(_root,
                                                 text=language_strings.TEXT_7,
                                                 width=300,
                                                 height=300)
    _measurementSettingFrame.place(x=600, y=90)
    _measurementSettingFrame.configure(font=('', 0, 'bold'), background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

    # Labels
    _generatedSignalTitleLabel = Tkinter.Label(_measurementSettingFrame, text=language_strings.TEXT_8,
                                              justify=Tkinter.LEFT)
    _generatedSignalTitleLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _generatedSignalTitleLabel.place(x=20, y=10)

    _generatedSignalMLSLengthLabel = Tkinter.Label(_measurementSettingFrame, text=language_strings.TEXT_9,
                                                  justify=Tkinter.LEFT)
    _generatedSignalMLSLengthLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _generatedSignalMLSLengthLabel.place(x=30, y=40)

    _generatedSignalAmplitudeLabel = Tkinter.Label(_measurementSettingFrame, text=language_strings.TEXT_10,
                                                  justify=Tkinter.LEFT)
    _generatedSignalAmplitudeLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _generatedSignalAmplitudeLabel.place(x=30, y=70)

    _generatedSignalPlaybackDelayLabel = Tkinter.Label(_measurementSettingFrame, text=language_strings.TEXT_11,
                                                      justify=Tkinter.LEFT)
    _generatedSignalPlaybackDelayLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _generatedSignalPlaybackDelayLabel.place(x=30, y=100)

    _recordedSignalTitleLabel = Tkinter.Label(_measurementSettingFrame, text=language_strings.TEXT_12,
                                             justify=Tkinter.LEFT)
    _recordedSignalTitleLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _recordedSignalTitleLabel.place(x=20, y=150)

    _recordedSignalDelayLabel = Tkinter.Label(_measurementSettingFrame, text=language_strings.TEXT_13,
                                             justify=Tkinter.LEFT)
    _recordedSignalDelayLabel.configure(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _recordedSignalDelayLabel.place(x=30, y=180)

    # Inputs
    _userValues_mlsLength = Tkinter.StringVar()
    _mlsLengthInputEntry = Tkinter.Entry(_measurementSettingFrame, width=8,
                                        textvariable=_userValues_mlsLength, justify=Tkinter.RIGHT)
    _mlsLengthInputEntry.config(highlightbackground=BACKGROUND_COLOR,
                               background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _mlsLengthInputEntry.place(x=200, y=40)

    _userValues_amplitude = Tkinter.StringVar()
    _amplitudeInputEntry = Tkinter.Entry(_measurementSettingFrame, width=8,
                                        textvariable=_userValues_amplitude, justify=Tkinter.RIGHT)
    _amplitudeInputEntry.config(highlightbackground=BACKGROUND_COLOR,
                               background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _amplitudeInputEntry.place(x=200, y=70)

    _userValues_predelay = Tkinter.StringVar()
    _predelayInputEntry = Tkinter.Entry(_measurementSettingFrame, width=8,
                                       textvariable=_userValues_predelay, justify=Tkinter.RIGHT)
    _predelayInputEntry.config(highlightbackground=BACKGROUND_COLOR,
                              background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _predelayInputEntry.place(x=200, y=100)

    _userValues_decay = Tkinter.StringVar()
    _decayInputEntry = Tkinter.Entry(_measurementSettingFrame, width=8,
                                    textvariable=_userValues_decay, justify=Tkinter.RIGHT)
    _decayInputEntry.config(highlightbackground=BACKGROUND_COLOR,
                           background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _decayInputEntry.place(x=200, y=180)

    _measurementSettingsRecoverDefaultValuesButton = Tkinter.Button(_measurementSettingFrame,
                                                                    text=language_strings.TEXT_14,
                                                                    command=lambda: interface_callbacks.
                                                                    recoverDefaultValuesCallback(
                                                                        _userValues_mlsLength,
                                                                        _userValues_amplitude,
                                                                        _userValues_predelay,
                                                                        _userValues_decay,
                                                                        _averagesEntry_Variable,
                                                                        _plotOutputDataCheck,
                                                                        _saveDataToFileCheck,
                                                                        defaultMeasurementSetup,
                                                                        _channelModeVar,
                                                                        _hwIRCorrectionEnabledCheckVar,
                                                                        _hwCorrectionFilename_L_Variable,
                                                                        _hwCorrectionFilename_R_Variable))

    _measurementSettingsRecoverDefaultValuesButton.config(highlightbackground=BACKGROUND_COLOR,
                                                         bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    _measurementSettingsRecoverDefaultValuesButton.place(x=20, y=230)

    _measurementSettingsValidateNumbersButton = Tkinter.Button(_measurementSettingFrame,
                                                              text=language_strings.TEXT_15,
                                                              command=lambda: interface_callbacks.
                                                              validateNumbersCallback(_userValues_mlsLength,
                                                                                      _userValues_amplitude,
                                                                                      _userValues_predelay,
                                                                                      _userValues_decay))
    _measurementSettingsValidateNumbersButton.config(highlightbackground=BACKGROUND_COLOR,
                                                    bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    _measurementSettingsValidateNumbersButton.place(x=150, y=230)

    # -----------------------
    #  Frame 3 - Output data
    # -----------------------

    _outputDataFrame = Tkinter.LabelFrame(_root,
                                         text=language_strings.TEXT_16,
                                         width=450,
                                         height=135)
    _outputDataFrame.place(x=10, y=395)
    _outputDataFrame.configure(font=('', 0, 'bold'), background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

    # Save to file options
    _saveDataToFileCheck = Tkinter.IntVar()
    _saveDataToFileCheck.set(False)

    _saveDataToFileCheckButton = Tkinter.Checkbutton(_outputDataFrame, text="", variable=_saveDataToFileCheck)
    _saveDataToFileCheckButton.configure(background=BACKGROUND_COLOR)
    _saveDataToFileCheckButton.place(x=10, y=10)

    _saveDataToFileLabel = Tkinter.Label(_outputDataFrame, text=language_strings.TEXT_17)
    _saveDataToFileLabel.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _saveDataToFileLabel.place(x=35, y=10)

    _saveDataToFile_variable = Tkinter.StringVar()
    interface_callbacks.recoverDefaultOutputFilename(_saveDataToFile_variable, defaultMeasurementSetup)
    _saveDataToFileEntry = Tkinter.Entry(_outputDataFrame, textvariable=_saveDataToFile_variable, width=40)
    _saveDataToFileEntry.config(background=BACKGROUND_COLOR,
                               foreground=FOREGROUND_COLOR, highlightbackground=BACKGROUND_COLOR, justify=Tkinter.RIGHT)
    _saveDataToFileEntry.place(x=35, y=40)

    _saveDataToFileButton = Tkinter.Button(_outputDataFrame,
                                          width=2, text=language_strings.TEXT_18,
                                          command=lambda: interface_callbacks.
                                          saveDataToFileCallback(_saveDataToFile_variable))
    _saveDataToFileButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    _saveDataToFileButton.place(x=380, y=40)

    # Plot output data options
    _plotOutputDataCheck = Tkinter.IntVar()
    _plotOutputDataCheck.set(True)

    _plotOutputDataCheckButton = Tkinter.Checkbutton(_outputDataFrame, text="", variable=_plotOutputDataCheck)
    _plotOutputDataCheckButton.configure(background=BACKGROUND_COLOR)
    _plotOutputDataCheckButton.place(x=10, y=80)

    _plotOutputDataLabel = Tkinter.Label(_outputDataFrame, text=language_strings.TEXT_19)
    _plotOutputDataLabel.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _plotOutputDataLabel.place(x=35, y=80)

    # ---------------------------------
    #  Frame 4 - Channel configuration
    # ---------------------------------

    _executeMeasurementFrame = Tkinter.LabelFrame(_root,
                                                  text=language_strings.TEXT_20,
                                                  width=430,
                                                  height=135)
    _executeMeasurementFrame.place(x=470, y=395)
    _executeMeasurementFrame.configure(font=('', 0, 'bold'), background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

    _channelModeLabel = Tkinter.Label(_executeMeasurementFrame, text=language_strings.TEXT_43)
    _channelModeLabel.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _channelModeLabel.place(x=20, y=10)

    _channelModeVar = Tkinter.IntVar()
    _channelModeVar.set(0)
    _channelModeVar.trace("w", lambda *args: setChildWidgetsEnabled(_hwIRCorrectionFrame, enabled=_channelModeVar.get()))
    _singleChannelModeRadioButton = Tkinter.Radiobutton(_executeMeasurementFrame, text="",
                                                        variable=_channelModeVar, value=0,
                                                        command=lambda: setChildWidgetsEnabled(_hwIRCorrectionFrame, False))
    _singleChannelModeRadioButton.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _singleChannelModeRadioButton.place(x=40, y=40)
    _singleChannelModeLabel = Tkinter.Label(_executeMeasurementFrame, text=language_strings.TEXT_44)
    _singleChannelModeLabel.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _singleChannelModeLabel.place(x=70, y=40)

    _dualChannelModeRadioButton = Tkinter.Radiobutton(_executeMeasurementFrame, text="",
                                                      variable=_channelModeVar, value=1,
                                                      command=lambda: setChildWidgetsEnabled(_hwIRCorrectionFrame, True))
    _dualChannelModeRadioButton.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _dualChannelModeRadioButton.place(x=40, y=70)
    _dualChannelModeLabel = Tkinter.Label(_executeMeasurementFrame, text=language_strings.TEXT_45)
    _dualChannelModeLabel.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _dualChannelModeLabel.place(x=70, y=70)

    _preAveragesLabel = Tkinter.Label(_executeMeasurementFrame, text=language_strings.TEXT_22)
    _preAveragesLabel.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _preAveragesLabel.place(x=230, y=10)

    _averagesEntry_Variable = Tkinter.StringVar()
    _averagesEntry_Variable.set("1")
    _averagesEntry = Tkinter.Entry(_executeMeasurementFrame, textvariable=_averagesEntry_Variable, width=8)
    _averagesEntry.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR,
                          highlightbackground=BACKGROUND_COLOR,  justify=Tkinter.RIGHT)
    _averagesEntry.place(x=345, y=10)

    _shouldStartMeasurementVar = Tkinter.BooleanVar()
    _shouldStartMeasurementVar.set(False)
    _executeMeasurementButton = Tkinter.Button(_executeMeasurementFrame, text=language_strings.TEXT_21,
                                              command=lambda: interface_callbacks.
                                              startMeasurement(_root,
                                                               bool(_plotOutputDataCheck.get()),
                                                               bool(_saveDataToFileCheck.get()),
                                                               _saveDataToFile_variable.get(),
                                                               _shouldStartMeasurementVar))
    _executeMeasurementButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    _executeMeasurementButton.place(x=350, y=80)

    # ----------------------------
    #  Frame 5 - HW IR Correction
    # ----------------------------

    _hwIRCorrectionFrame = Tkinter.LabelFrame(_root,
                                                  text=language_strings.TEXT_46,
                                                  width=300,
                                                  height=150)
    _hwIRCorrectionFrame.place(x=910, y=90)
    _hwIRCorrectionFrame.configure(font=('', 0, 'bold'), background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

    _hwIRCorrectionEnabled_Label = Tkinter.Label(_hwIRCorrectionFrame, text=language_strings.TEXT_51)
    _hwIRCorrectionEnabled_Label.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _hwIRCorrectionEnabled_Label.place(x=40, y=10)
    _hwIRCorrectionEnabledCheckVar = Tkinter.IntVar()
    _hwIRCorrectionEnabledCheckVar.set(False)
    _hwIRCorrectionEnabledCheck = Tkinter.Checkbutton(_hwIRCorrectionFrame, text="", variable=_hwIRCorrectionEnabledCheckVar)
    _hwIRCorrectionEnabledCheck.configure(background=BACKGROUND_COLOR)
    _hwIRCorrectionEnabledCheck.place(x=10, y=10)



    _hwIRCorrection_L_Label = Tkinter.Label(_hwIRCorrectionFrame, text=language_strings.TEXT_47)
    _hwIRCorrection_L_Label.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _hwIRCorrection_L_Label.place(x=10, y=47)
    _hwCorrectionFilename_L_Variable = Tkinter.StringVar()
    _hwCorrectionFilename_L_Variable.set("")
    _hwCorrection_L_Entry = Tkinter.Entry(_hwIRCorrectionFrame, textvariable=_hwCorrectionFilename_L_Variable, width=25)
    _hwCorrection_L_Entry.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR,
                          highlightbackground=BACKGROUND_COLOR,  justify=Tkinter.RIGHT)
    _hwCorrection_L_Entry.place(x=30, y=45)

    _loadHWIRCorrection_L_Button = Tkinter.Button(_hwIRCorrectionFrame, text=language_strings.TEXT_49)
    _loadHWIRCorrection_L_Button.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                        command=lambda: interface_callbacks.
                                        openFileCallback(_hwCorrectionFilename_L_Variable))
    _loadHWIRCorrection_L_Button.place(x=245, y=45)

    _hwIRCorrection_R_Label = Tkinter.Label(_hwIRCorrectionFrame, text=language_strings.TEXT_48)
    _hwIRCorrection_R_Label.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
    _hwIRCorrection_R_Label.place(x=10, y=87)
    _hwCorrectionFilename_R_Variable = Tkinter.StringVar()
    _hwCorrectionFilename_R_Variable.set("")
    _hwCorrection_R_Entry = Tkinter.Entry(_hwIRCorrectionFrame, textvariable=_hwCorrectionFilename_R_Variable, width=25)
    _hwCorrection_R_Entry.config(background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR,
                          highlightbackground=BACKGROUND_COLOR,  justify=Tkinter.RIGHT)
    _hwCorrection_R_Entry.place(x=30, y=85)

    _loadHWIRCorrection_R_Button = Tkinter.Button(_hwIRCorrectionFrame, text=language_strings.TEXT_50)
    _loadHWIRCorrection_R_Button.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                        command=lambda: interface_callbacks.
                                        openFileCallback(_hwCorrectionFilename_R_Variable))
    _loadHWIRCorrection_R_Button.place(x=245, y=85)

    # -- Status bar --

    _status = Tkinter.Label(_root, text=language_strings.TEXT_23,
                           bd=1, relief=Tkinter.SUNKEN, anchor=Tkinter.W)
    _status.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)

    # ---------------------------
    #  Loads data into interface
    # ---------------------------


    # Sets default values
    interface_callbacks.recoverDefaultValuesCallback(_userValues_mlsLength, _userValues_amplitude,
                                                     _userValues_predelay, _userValues_decay,
                                                     _averagesEntry_Variable, _plotOutputDataCheck,
                                                     _saveDataToFileCheck, defaultMeasurementSetup,
                                                     _channelModeVar,
                                                     _hwIRCorrectionEnabledCheckVar,
                                                     _hwCorrectionFilename_L_Variable,
                                                     _hwCorrectionFilename_R_Variable)
    
    # Loads combos
    _loadDeviceLists(_inputDeviceCombo, _inputDevicesVar, _outputDeviceCombo, _outputDevicesVar)
    
    # Gives control to window manager
    _root.mainloop()

    if bool(_shouldStartMeasurementVar.get()):
        _measurementSettings = type_classes.MeasurementSettings()

        _measurementSettings.MLSLength = int(_userValues_mlsLength.get())
        _measurementSettings.inputDeviceSamplFreq = int(selectedInputInterface.samplingRates[0])
        _measurementSettings.outputDeviceSamplFreq = int(selectedOutputInterface.samplingRates[0])
        _measurementSettings.signalAmplitude = float(_userValues_amplitude.get())
        _measurementSettings.preDelayForPlayback = float(_userValues_predelay.get())
        _measurementSettings.decayTime = float(_userValues_decay.get())
        _measurementSettings.inputDevice = selectedInputInterface.interfaceID
        _measurementSettings.outputDevice = selectedOutputInterface.interfaceID

        _measurementSettings.shouldPlot = bool(_plotOutputDataCheck.get())
        _measurementSettings.shouldSaveToFile = bool(_saveDataToFileCheck.get())
        _measurementSettings.shouldSaveToFileFilename = _saveDataToFile_variable.get()
        _measurementSettings.numberOfPreAverages = int(_averagesEntry_Variable.get())

        if _channelModeVar.get():
            _measurementSettings.dualChannelMode = True

        _measurementSettings.hwCorrectionFilename_L = _hwCorrectionFilename_L_Variable.get()
        _measurementSettings.hwCorrectionFilename_R = _hwCorrectionFilename_R_Variable.get()
        _measurementSettings.shouldUseHWCorrection = _hwIRCorrectionEnabledCheckVar.get()

        return _measurementSettings

    else:
        return False
