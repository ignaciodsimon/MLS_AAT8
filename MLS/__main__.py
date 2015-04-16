"""
Application entry point.

Joe.
"""


# Adds parent directory to path, for the internal imports
import os
import sys
# parent = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent)

# Python imports
import multiprocessing as mp

# Private imports
from interface_layer import interface, plotting
from logic_layer import measurement, results_handling
# from type_classes import type_classes
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
    while not isinstance(_returnedValue, bool):

        # Executes the measurement(s)
        print language_strings.TEXT_36
        measurementResult = measurement.executeMeasurement(_returnedValue)
        print language_strings.TEXT_37

        # Saves the output if necessary
        if _returnedValue.shouldSaveToFile:
            print language_strings.TEXT_38
            results_handling.saveResultsToFile(measurementResult)
            print language_strings.TEXT_39

        # Plots the output if necessary
        if _returnedValue.shouldPlot:
            print language_strings.TEXT_40
            _pool = mp.Pool()
            _result1 = _pool.apply_async(plotting.plotResults, [measurementResult])
            _pool.close()
            _pool.join()
            # plotting.plotResults(measurementResult)
            print language_strings.TEXT_41

        _pool = mp.Pool()
        _result1 = _pool.apply_async(interface.buildInterface, [_returnedValue])
        _returnedValue = _result1.get()
        _pool.close()
        _pool.join()
