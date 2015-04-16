
import numpy
import scipy.io.wavfile as wav
import struct
#import MLS.logic_layer.player as player
#import matplotlib.pyplot as plot
#from matplotlib.backends.backend_pdf import PdfPages


def readWavfile(filename):
    """
    Reads an wave file.

    Christian
    :param filename: Path and filename to wav.
    :return: Vector containing wav samplerate and data.
    """
    (samplerate, data) = wav.read(filename)

    return samplerate, data


#
# print "Reading IRs from file ..."
# non_weighted_IR = readWavImpulseResponseFile("meas_nonweighted_1s_03.wav")
# A_weighted_IR = readWavImpulseResponseFile("meas_Aweighted_1_5s_02.wav")
#
# print "Trimming IRs ..."
# non_weighted_IR = non_weighted_IR[0:int(len(non_weighted_IR)/2)]
# A_weighted_IR = A_weighted_IR[0:len(non_weighted_IR)]
#
# # plot.subplot(2, 1, 1)
# # plot.plot(non_weighted_IR)
# # plot.subplot(2, 1, 2)
# # plot.plot(A_weighted_IR)
# # plot.show()
#
# print "Saving plots to PDF ..."
# fig = plot.figure(dpi=60)
# F = plot.gcf()
# Size = F.get_size_inches()
# F.set_size_inches(8, 4)
# plot.grid()
# plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
# plot.plot(non_weighted_IR)
# plot.xlabel("Samples")
# plot.ylabel("Amplitude")
# plot.title("Non-weighted IR on noisy environment (SNR < 3dB)")
# pp = PdfPages('non_weighted_IR.pdf')
# pp.savefig(fig)
# pp.close()
#
# fig = plot.figure(dpi=60)
# F = plot.gcf()
# Size = F.get_size_inches()
# F.set_size_inches(8, 4)
# plot.grid()
# plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
# plot.plot(A_weighted_IR)
# plot.xlabel("Samples")
# plot.ylabel("Amplitude")
# plot.title("A-weighted IR on noisy environment (SNR < 3dB)")
# pp = PdfPages('A_weighted_IR.pdf')
# pp.savefig(fig)
# pp.close()
