"""
Application entry point.
"""


import interface
import measurement
import multiprocessing as mp
import write_wav
import plotting
import strings


if __name__ == "__main__":

    # Shows version and basic software information.
    print strings.TEXT_0 + "\n" + strings.TEXT_23 + "\n" + strings.TEXT_42 + "\n"

    # Included to support the multiprocessing on Windows machines
    mp.freeze_support()

    # Runs the interface in another process to "fix" the bug between Tkinter and audio core libraries
    _pool = mp.Pool()
    _result1 = _pool.apply_async(interface.buildInterface)
    _returnedValue = _result1.get()
    _pool.close()
    _pool.join()

    # Checks if window was closed or if the "start" button was clicked
    if isinstance(_returnedValue, measurement.MeasurementSettings):

        # Executes the measurement(s)
        print strings.TEXT_36
        measurementResult = measurement.executeMeasurement(_returnedValue)
        print strings.TEXT_37

        # Saves the output if necessary
        if _returnedValue.shouldSaveToFile:
            print strings.TEXT_38
            write_wav.saveImpulseResponseToWav(measurementResult)
            print strings.TEXT_39

        # Plots the output if necessary
        if _returnedValue.shouldPlot:
            print strings.TEXT_40
            plotting.plotResults(measurementResult)
            print strings.TEXT_41
