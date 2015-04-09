"""
Application entry point.
"""

import multiprocessing as mp

from python.interface_layer import interface, plotting
from python.logic_layer import measurement
from python.data_layer import write_wav
import language_strings


if __name__ == "__main__":

    # Shows version and basic software information.
    print language_strings.TEXT_0 + "\n" + language_strings.TEXT_23 + "\n" + language_strings.TEXT_42 + "\n"

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
        print language_strings.TEXT_36
        measurementResult = measurement.executeMeasurement(_returnedValue)
        print language_strings.TEXT_37

        # Saves the output if necessary
        if _returnedValue.shouldSaveToFile:
            print language_strings.TEXT_38
            write_wav.saveImpulseResponseToWav(measurementResult)
            print language_strings.TEXT_39

        # Plots the output if necessary
        if _returnedValue.shouldPlot:
            print language_strings.TEXT_40
            plotting.plotResults(measurementResult)
            print language_strings.TEXT_41
