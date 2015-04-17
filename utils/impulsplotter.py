
import numpy
import scipy.io.wavfile as wav
import math
import struct
#import MLS.logic_layer.player as player
import matplotlib.pyplot as plot
from matplotlib.backends.backend_pdf import PdfPages

print "Type the path of the .wav file to be plotted:"
filename = raw_input("")


def readWavfile(filename):
    """
    Reads an wave file.

    Christian
    :param filename: Path and filename to wav.
    :return: Vector containing .wav samplerate and data.
    """
    print "Reading .wav file file..."
    (samplerate, data) = wav.read(filename)
    print "Done reading .wav file..."

    return samplerate, data

(samplerate, data) = readWavfile(filename)

# #compute time vector
# time = len(data)/samplerate
# timevector = numpy.linspace(0, len(data), time*samplerate)
# print len(timevector), len(data)

#Normalize data
print "Do you want to normalize the data? y/n"
ans = raw_input("")

if ans == 'y':
    print "Normalizing..."
    data = numpy.divide(data, float(max(data)))
    print "Done normalizing..."
else:
    data = data

print "Do you want to trim the length? y/n"
ans = raw_input("")
if ans == 'y':
    print "How much to keep in percentage? From 0-1"
    trim = raw_input()
    trim = float(trim)
    newlength = len(data)*trim
    print "Trimming..."
    data = data[:math.floor(newlength)]
    print "Done trimming..."
    print "Keeping the first", len(data), "samples"
else:
    data = data



print "Saving to pdf..."
fig = plot.figure(dpi=60)
F = plot.gcf()
Size = F.get_size_inches()
F.set_size_inches(8, 4)
plot.grid()
plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
plot.plot(data)
plot.xlabel("Samples")
plot.ylabel("Amplitude")
pp = PdfPages(filename+'.pdf')
pp.savefig(fig)
pp.close()
print "Done saving..."