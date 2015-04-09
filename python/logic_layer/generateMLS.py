"""
Functions to generate MLS signals that can be used for impulse-response measuring.

Function:
    generateMLS(sequenceLength=16000, amplitude=1)

Joe.
"""

import numpy


def generateMLS(sequenceLength=16000, amplitude=pow(10, -3.0/20)):
    """
    Generates a MLS (Maximum Length Sequence) with corrected (zero) mean of the given sequence length.
    If the given sequence length is not standard (a power of two), it would be corrected to the closest
    value.

    Joe.
    :param sequenceLength: Length in samples, ideally a power of two
    :return: Generated signal
    """

    # Limits amplitude to -3 dBFS to prevent output saturation
    if amplitude > pow(10, -3.0/20):
        amplitude = pow(10, -3.0/20)

    # Normalizes the sequence length
    _sequenceBits = numpy.int(numpy.ceil(1.0 * numpy.log10(sequenceLength) / numpy.log10(2)))
    sequenceLength = pow(2, _sequenceBits)

    # Creates the registers
    _mlsRegisters = [1]*_sequenceBits
    _mlsSignal = [0]*sequenceLength

    for n in range(sequenceLength):
        # Last takes the value of first plus second
        _sumValue = numpy.bitwise_xor(_mlsRegisters[0], _mlsRegisters[1])

        # Rotates all registers
        _mlsRegisters = _mlsRegisters[1:] + _mlsRegisters[:1]

        # Updates last value
        _mlsRegisters[len(_mlsRegisters)-1] = _sumValue

        # Saves current output
        _mlsSignal[n] = _mlsRegisters[0]

    # Corrects generated signal to obtain zero mean
    _mlsSignal = _mlsSignal - numpy.mean(_mlsSignal)

    # Corrects signal to desired amplitude
    _mlsSignal = numpy.dot(_mlsSignal, amplitude)

    return _mlsSignal
