"""
Application entry point.
"""


import interface
import measurement
import multiprocessing as mp
import matplotlib.pyplot as plot

# Runs the interface in another process to "fix" the bug between Tkinter and audio core libraries
_pool = mp.Pool()
_result1 = _pool.apply_async(interface.buildInterface)
_returnedValue = _result1.get()
_pool.close()
_pool.join()

# Checks if window was closed or if the "start" button was clicked
if isinstance(_returnedValue, measurement.MeasurementSettings):

    print _returnedValue.MLSLength
    print _returnedValue.inputDeviceSamplFreq
    print _returnedValue.outputDeviceSamplFreq
    print _returnedValue.signalAmplitude
    print _returnedValue.preDelayForPlayback
    print _returnedValue.decayTime
    print _returnedValue.inputDevice
    print _returnedValue.outputDevice

    print _returnedValue.shouldPlot
    print _returnedValue.shouldSaveToFile
    print _returnedValue.shouldSaveToFileFilename

    settings = measurement.MeasurementSettings()
    measurementResult = measurement.executeMeasurement(settings)

    if _returnedValue.shouldSaveToFile:
        # TODO: complete this part
        print "Save results to file here"

    if _returnedValue.shouldPlot:
        # TODO: make the plot a bit more beautiful ...
        plot.plot(measurementResult.computedImpulseResponse)
        plot.show()
