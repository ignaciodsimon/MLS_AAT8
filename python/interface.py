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

data = recorder.rec(_channels=2, _duration=60000, _fs=44100, _nbits=16)

print numpy.shape(data)
# plot.plot(data)
# plot.show()
