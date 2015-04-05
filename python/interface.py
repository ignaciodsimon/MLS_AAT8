import matplotlib.pyplot as plot
import Tkinter
import tkMessageBox
import tkFileDialog


# Internal imports
import measurement


# Global constants
DEFAULT_VALUES_MLS_LENGTH = 32768
DEFAULT_VALUES_AMPLITUDE = 0.5
DEFAULT_VALUES_PLAYBACK_PREDELAY = 250
DEFAULT_VALUES_EXPECTED_DECAY = 5.0
DEFAULT_VALUES_OUTPUT_FILENAME = "outputFile.txt"

BACKGROUND_COLOR = "#10547F"
# BACKGROUND_COLOR = "#00446f"
TEXT_COLOR = "#FFFFFF"


# Callback functions
def recoverDefaultValuesCallback():
    """
    Callback function for "Recover default values" button on section 2 "measurement settings".

    Joe.
    :return: Nothing.
    """
    userValues_mlsLength.set(DEFAULT_VALUES_MLS_LENGTH)
    userValues_amplitude.set(DEFAULT_VALUES_AMPLITUDE)
    userValues_predelay.set(DEFAULT_VALUES_PLAYBACK_PREDELAY)
    userValues_decay.set(DEFAULT_VALUES_EXPECTED_DECAY)


# TODO: complete this
def validateNumbersCallback():
    tkMessageBox.showinfo('Debug ...', 'Complete this part validating the numbers in the entries ...')


# TODO: complete this
def testInputDeviceCallback():
    tkMessageBox.showinfo('Debug ...', 'Complete this part with an input level test ...')


# TODO: complete this
def testOutputDeviceCallback():
    tkMessageBox.showinfo('Debug ...', 'Complete this part with an output signal test ...')


# TODO: complete this
def saveDataToFileCallback():

    _filename = tkFileDialog.asksaveasfilename(defaultextension=".txt")

    if _filename != "":
        print "Selected to save as: ", _filename
    else:
        print "No file selected ..."
    # tkMessageBox.showinfo('Debug ...', 'Complete this part with a save dialog ...')


# TODO: complete this
def startMeasurement():
    # Must:
    # - verify parameters
    # - show a "please wait" dialog
    # - call measurement and wait for return data
    # - display a plot and / or save data to file
    tkMessageBox.showinfo('Debug ...', 'Complete this part performing the measurement')


# Root window
root = Tkinter.Tk()
root.title("Impulse response measuring system - AAU 2015")
root.resizable(width=False, height=False)
root.geometry("910x570")
root.configure(padx=0, pady=0, background=BACKGROUND_COLOR)

logo = Tkinter.PhotoImage(file="top_banner.gif")
w1 = Tkinter.Label(root, image=logo)
w1.configure(background=BACKGROUND_COLOR, padx=0, pady=0)
w1.place(x=0, y=0)


# -----------------------------
#  Frame 1 - Hardware settings
# -----------------------------
hardwareSettingFrame = Tkinter.LabelFrame(root,
                                          text="  1 - Hardware settings  ",
                                          width=580,
                                          height=300)
hardwareSettingFrame.configure(background=BACKGROUND_COLOR)
hardwareSettingFrame.place(x=10, y=90)
hardwareSettingFrame.configure(font=('', 0, 'bold'), foreground=TEXT_COLOR)

# Input / output devices labels
hdwInputLabel = Tkinter.Label(hardwareSettingFrame, text="Input device:")
hdwInputLabel.place(x=20, y=10, anchor="nw")
hdwInputLabel.configure(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
hdwOutputLabel = Tkinter.Label(hardwareSettingFrame, text="Output device:")
hdwOutputLabel.place(x=300, y=10, anchor="nw")
hdwOutputLabel.configure(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)

# Input / output devices combos
inputDevicesList = Tkinter.StringVar(hardwareSettingFrame)
inputDevicesList.set("- No devices -")
inputDeviceCombo = Tkinter.OptionMenu(hardwareSettingFrame, inputDevicesList, "- No devices -")
inputDeviceCombo.config(width=24, background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
inputDeviceCombo.place(x=20, y=30)

outputDevicesList = Tkinter.StringVar(hardwareSettingFrame)
outputDevicesList.set("- No devices -")
outputDeviceCombo = Tkinter.OptionMenu(hardwareSettingFrame, outputDevicesList, "- No devices -")
outputDeviceCombo.config(width=24, background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
outputDeviceCombo.place(x=300, y=30)

# Test buttons
testInputDeviceButton = Tkinter.Button(hardwareSettingFrame, text="Test", width=2, command=testInputDeviceCallback)
testInputDeviceButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
testInputDeviceButton.place(x=230, y=30)

testOutputDeviceButton = Tkinter.Button(hardwareSettingFrame, text="Test", width=2, command=testOutputDeviceCallback)
testOutputDeviceButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
testOutputDeviceButton.place(x=510, y=30)

# Input /output devices properties labels
inputDeviceLabel = Tkinter.Label(hardwareSettingFrame,
                                 text="Sampling rates [Hz]: \n"
                                      "  --\n"
                                      "Bit depths [bit]:\n"
                                      "  --\n"
                                      "Input channels:\n"
                                      "  --\n"
                                      "Output channels:\n"
                                      "  --\n"
                                      "Input latency [ms]:\n"
                                      "  --\n"
                                      "Output latency [ms]:\n"
                                      "  --",
                                 justify=Tkinter.LEFT)
inputDeviceLabel.configure(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
inputDeviceLabel.place(x=20, y=70)

outputDeviceLabel = Tkinter.Label(hardwareSettingFrame,
                                 text="Sampling rates [Hz]: \n"
                                      "  --\n"
                                      "Bit depths [bit]:\n"
                                      "  --\n"
                                      "Input channels:\n"
                                      "  --\n"
                                      "Output channels:\n"
                                      "  --\n"
                                      "Input latency [ms]:\n"
                                      "  --\n"
                                      "Output latency [ms]:\n"
                                      "  --",
                                 justify=Tkinter.LEFT)
outputDeviceLabel.configure(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
outputDeviceLabel.place(x=300, y=70)


# --------------------------------
#  Frame 2 - Measurement settings
# --------------------------------
measurementSettingFrame = Tkinter.LabelFrame(root,
                                             text="  2 - Measurement settings  ",
                                             width=300,
                                             height=300)
measurementSettingFrame.place(x=600, y=90)
measurementSettingFrame.configure(font=('', 0, 'bold'), background=BACKGROUND_COLOR, foreground=TEXT_COLOR)

# Labels
generatedSignalTitleLabel = Tkinter.Label(measurementSettingFrame, text="Generated signal", justify=Tkinter.LEFT)
generatedSignalTitleLabel.configure(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
generatedSignalTitleLabel.place(x=20, y=10)

generatedSignalMLSLengthLabel = Tkinter.Label(measurementSettingFrame, text="MLS length [samples]:", justify=Tkinter.LEFT)
generatedSignalMLSLengthLabel.configure(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
generatedSignalMLSLengthLabel.place(x=30, y=40)

generatedSignalAmplitudeLabel = Tkinter.Label(measurementSettingFrame, text="Amplitude (0.0 - 1.0):", justify=Tkinter.LEFT)
generatedSignalAmplitudeLabel.configure(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
generatedSignalAmplitudeLabel.place(x=30, y=70)

generatedSignalPlaybackDelayLabel = Tkinter.Label(measurementSettingFrame, text="Playback pre-delay [ms]:", justify=Tkinter.LEFT)
generatedSignalPlaybackDelayLabel.configure(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
generatedSignalPlaybackDelayLabel.place(x=30, y=100)

recordedSignalTitleLabel = Tkinter.Label(measurementSettingFrame, text="Recorded signal", justify=Tkinter.LEFT)
recordedSignalTitleLabel.configure(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
recordedSignalTitleLabel.place(x=20, y=150)

recordedSignalDelayLabel = Tkinter.Label(measurementSettingFrame, text="Expected decay time [s]:", justify=Tkinter.LEFT)
recordedSignalDelayLabel.configure(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
recordedSignalDelayLabel.place(x=30, y=180)

# Inputs
userValues_mlsLength = Tkinter.StringVar()
userValues_mlsLength.set(DEFAULT_VALUES_MLS_LENGTH)
mlsLengthInputEntry = Tkinter.Entry(measurementSettingFrame, width=8, textvariable=userValues_mlsLength, justify=Tkinter.RIGHT)
mlsLengthInputEntry.config(highlightbackground=BACKGROUND_COLOR, background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
mlsLengthInputEntry.place(x=200, y=40)

userValues_amplitude = Tkinter.StringVar()
userValues_amplitude.set(DEFAULT_VALUES_AMPLITUDE)
amplitudeInputEntry = Tkinter.Entry(measurementSettingFrame, width=8, textvariable=userValues_amplitude, justify=Tkinter.RIGHT)
amplitudeInputEntry.config(highlightbackground=BACKGROUND_COLOR, background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
amplitudeInputEntry.place(x=200, y=70)

userValues_predelay = Tkinter.StringVar()
userValues_predelay.set(DEFAULT_VALUES_PLAYBACK_PREDELAY)
predelayInputEntry = Tkinter.Entry(measurementSettingFrame, width=8, textvariable=userValues_predelay, justify=Tkinter.RIGHT)
predelayInputEntry.config(highlightbackground=BACKGROUND_COLOR, background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
predelayInputEntry.place(x=200, y=100)

userValues_decay = Tkinter.StringVar()
userValues_decay.set(DEFAULT_VALUES_EXPECTED_DECAY)
decayInputEntry = Tkinter.Entry(measurementSettingFrame, width=8, textvariable=userValues_decay, justify=Tkinter.RIGHT)
decayInputEntry.config(highlightbackground=BACKGROUND_COLOR, background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
decayInputEntry.place(x=200, y=180)


measurementSettingsRecoverDefaultValuesButton = Tkinter.Button(measurementSettingFrame, text="Recover default", command=recoverDefaultValuesCallback)
measurementSettingsRecoverDefaultValuesButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
measurementSettingsRecoverDefaultValuesButton.place(x=20, y=230)

measurementSettingsValidateNumbersButton = Tkinter.Button(measurementSettingFrame, text="Validate numbers", command=validateNumbersCallback)
measurementSettingsValidateNumbersButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
measurementSettingsValidateNumbersButton.place(x=150, y=230)


# -----------------------
#  Frame 3 - Output data
# -----------------------
outputDataFrame = Tkinter.LabelFrame(root,
                                     text="  3 - Output data  ",
                                     width=450,
                                     height=135)
outputDataFrame.place(x=10, y=395)
outputDataFrame.configure(font=('', 0, 'bold'), background=BACKGROUND_COLOR, foreground=TEXT_COLOR)

# Save to file options
saveDataToFileCheck = Tkinter.IntVar()
saveDataToFileCheck.set(False)

saveDataToFileCheckButton = Tkinter.Checkbutton(outputDataFrame, text="", variable=saveDataToFileCheck)
saveDataToFileCheckButton.configure(background=BACKGROUND_COLOR)
saveDataToFileCheckButton.place(x=10, y=10)

saveDataToFileLabel = Tkinter.Label(outputDataFrame, text="Save data to text file:")
saveDataToFileLabel.config(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
saveDataToFileLabel.place(x=35, y=10)

saveDataToFile_variable = Tkinter.StringVar()
saveDataToFile_variable.set(DEFAULT_VALUES_OUTPUT_FILENAME)

saveDataToFileEntry = Tkinter.Entry(outputDataFrame, textvariable=saveDataToFile_variable, width=40)
saveDataToFileEntry.config(background=BACKGROUND_COLOR, foreground=TEXT_COLOR, highlightbackground=BACKGROUND_COLOR)
saveDataToFileEntry.place(x=35, y=40)

saveDataToFileButton = Tkinter.Button(outputDataFrame, width=2, text="...", command=saveDataToFileCallback)
saveDataToFileButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
saveDataToFileButton.place(x=380, y=40)

# Plot output data options
plotOutputDataCheck = Tkinter.IntVar()
plotOutputDataCheck.set(True)

plotOutputDataCheckButton = Tkinter.Checkbutton(outputDataFrame, text="", variable=plotOutputDataCheck)
plotOutputDataCheckButton.configure(background=BACKGROUND_COLOR)
plotOutputDataCheckButton.place(x=10, y=80)

plotOutputDataLabel = Tkinter.Label(outputDataFrame, text="Plot measured impulse response.")
plotOutputDataLabel.config(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
plotOutputDataLabel.place(x=35, y=80)


# -----------------------
#  Frame 4 - Output data
# -----------------------
executeMeasurementFrame = Tkinter.LabelFrame(root,
                                             text="  4 - Execute measurement  ",
                                             width=430,
                                             height=135)
executeMeasurementFrame.place(x=470, y=395)
executeMeasurementFrame.configure(font=('', 0, 'bold'), background=BACKGROUND_COLOR, foreground=TEXT_COLOR)

executeMeasurementButton = Tkinter.Button(executeMeasurementFrame, text="START", command=startMeasurement)
executeMeasurementButton.config(highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
executeMeasurementButton.place(x=40, y=20)

executeMeasurementLabel = Tkinter.Label(executeMeasurementFrame, text="Status: Idle.")
executeMeasurementLabel.config(background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
executeMeasurementLabel.place(x=40, y=60)

status = Tkinter.Label(root, text="MSc. Acoustics and Audio Technology, 2015 - Aalborg University", bd=1, relief=Tkinter.SUNKEN, anchor=Tkinter.W)
status.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)

root.mainloop()



















# myIR = measurement.executeMeasurement(MLSLength=32768,
#                                       inputDeviceSamplFreq=44100,
#                                       outputDeviceSamplFreq=44100,
#                                       signalAmplitude=0.5,
#                                       preDelayForPlayback=0.25,
#                                       decayTime=5.0,
#                                       inputDevice=-1,
#                                       outputDevice=-1)
# plot.plot(myIR)
# plot.show()
