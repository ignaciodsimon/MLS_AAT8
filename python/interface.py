"""
Main interface of the system.

Parts:
    - Initialization, checks if necessary
    - Obtaining of parameters from user
    - Adjustment of output signal level
    - Computation of IR from MLS signal and measurement(s)
    - Displaying / saving of results


Joe.
"""

import recorder
import numpy
import matplotlib.pyplot as plot

data = recorder.rec(numOfChannels=2, recordingLength=60000, samplFreq=44100, bitDepth=16)


# print data
print numpy.shape(data)
# plot.plot(data)
# plot.show()
