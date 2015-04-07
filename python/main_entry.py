"""
Application entry point.
"""


import interface
import measurement
import multiprocessing as mp
import write_wav
import plotting

if __name__ == "__main__":

    mp.freeze_support()

    # Runs the interface in another process to "fix" the bug between Tkinter and audio core libraries
    _pool = mp.Pool()
    _result1 = _pool.apply_async(interface.buildInterface)
    _returnedValue = _result1.get()
    _pool.close()
    _pool.join()

    # Checks if window was closed or if the "start" button was clicked
    if isinstance(_returnedValue, measurement.MeasurementSettings):

        print "Executing measurement ..."
        measurementResult = measurement.executeMeasurement(_returnedValue)
        print "Measurement done."

        if _returnedValue.shouldSaveToFile:
            print "Saving impulse response to Wav file ..."
            write_wav.saveImpulseResponseToWav(measurementResult.computedImpulseResponse,
                                     measurementResult.settings.inputDeviceSamplFreq,
                                     measurementResult.settings.shouldSaveToFileFilename,
                                     measurementResult.settings.normalizeOutput)
            print "Saving done."

        if _returnedValue.shouldPlot:
            # TODO: make the plot a bit more beautiful ...
            print "Plotting results ..."
            plotting.plotResults(measurementResult)

        print "All done."
