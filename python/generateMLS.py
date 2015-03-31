import numpy


def generateMLS(sequenceLength=16000):
    """
    Generates a MLS (Maximum Length Sequence) with corrected (zero) mean of the given sequence length.
    If the given sequence length is not standard (a power of two), it would be corrected to the closest
    value.

    Joe.
    :param sequenceLength: Length in samples, ideally a power of two
    :return: Generated signal
    """

    # Normalizes the sequence length
    sequenceBits = numpy.int(numpy.ceil(1.0 * numpy.log10(sequenceLength) / numpy.log10(2)))
    sequenceLength = pow(2, sequenceBits)

    # Creates the registers
    mls_registers = [1]*sequenceBits
    mls_signal = [0]*sequenceLength

    for n in range(sequenceLength):
        # Last takes the value of first plus second
        sumValue = numpy.bitwise_xor(mls_registers[0], mls_registers[1])

        # Rotates all registers
        mls_registers = mls_registers[1:] + mls_registers[:1]

        # Updates last value
        mls_registers[len(mls_registers)-1] = sumValue

        # Saves current output
        mls_signal[n] = mls_registers[0]

    # Corrects generated signal to obtain zero mean
    mls_signal = mls_signal - numpy.mean(mls_signal)

    return mls_signal
