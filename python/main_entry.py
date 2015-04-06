"""
Application entry point.
"""


import interface
import measurement
import matplotlib.pyplot as plot

# Builds interface and gives control to window manager
interface.buildInterface()

# import numpy
# # Generates the signals
# signal1 = [1.0 * numpy.sin(2 * numpy.pi * 1000 * n/44100) for n in range(44100)]
# signal2 = [1.0 * numpy.sin(2 * numpy.pi * 2000 * n/44100) for n in range(44100)]
#
# # Sends them to the sound card
# import player
# player.playSignals(signal1, signal2, samplingFreq=44100, normalize=False)


# settings = measurement.MeasurementSettings()

# settings.MLSLength = 1020
# settings.inputDeviceSamplFreq = 44100
# settings.outputDeviceSamplFreq = 44100
# settings.signalAmplitude = 0.5
# settings.preDelayForPlayback = 0.0
# settings.decayTime = 0.0
# settings.inputDevice = 1
# settings.outputDevice = 1

# data = measurement.executeMeasurement(settings)
# print "done measuring!"
# plot.plot(data.computedImpulseResponse)
# plot.show()
#
# print settings.MLSLength
# print settings.inputDeviceSamplFreq
# print settings.outputDeviceSamplFreq
# print settings.signalAmplitude
# print settings.preDelayForPlayback
# print settings.decayTime
# print settings.inputDevice
# print settings.outputDevice
