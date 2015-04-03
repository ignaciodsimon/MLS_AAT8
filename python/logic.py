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

import matplotlib.pyplot as plot

# Internal imports
import recorder
import parallelfunctions
import player
import computeIR
import generateMLS


# ----------= TEST CONFIGURATION =----------
_MLSLength = 32768
_channels = 2
_samplFreq = 44100
_signalAmplitude = 0.5
_preDelayForPlayback = 0.25
_decayTime = 5.0


# ----------= TEST EXECUTION =----------
# Generate the MLS signal
print "Generating MLS signal ..."
_MLSSignal = generateMLS.generateMLS(_MLSLength, _signalAmplitude)

# Padding MLS signal with zeros at the beginning
_MLS_WithZeros = [0] * int(round(_preDelayForPlayback * _samplFreq) + _MLSLength)
_MLS_WithZeros[len(_MLS_WithZeros)-len(_MLSSignal):len(_MLS_WithZeros)] = _MLSSignal
_MLSSignal = _MLS_WithZeros

# Recording length is function of MLS length and the system decay time
_recordingLength = len(_MLSSignal) + int(_samplFreq * _decayTime)

# Player and recorder input arguments in vectors for multitasking
_recorderArguments = [_channels, _recordingLength, _samplFreq, 16]
_playerArguments = [_MLSSignal, _MLSSignal, _samplFreq, False]

# Runs player and recorder simultaneously
print "Running multitask ..."
[_recorderOutputData, _playerOutputData] = parallelfunctions.runInParallel(recorder.rec, _recorderArguments, player.playSignals, _playerArguments)

# Computes IR
print "Computing IRs ..."
channelL = _recorderOutputData[0][:]
channelR = _recorderOutputData[1][:]

# Padding with zeros of MLS signal
_paddedMLSSignal = [0]*(len(channelL))
_paddedMLSSignal[0:len(_MLSSignal)] = _MLSSignal

_IRLeft = computeIR.computeCircularXCorr(channelL, _paddedMLSSignal)
_IRRight = computeIR.computeCircularXCorr(channelR, _paddedMLSSignal)
_corrected = computeIR.correctSignalWithIR(_IRLeft, _IRRight)


# ----------= DISPLAY OF RESULTS =----------
plot.plot(_corrected)
plot.show()