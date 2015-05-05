__author__ = 'Usuario'



import numpy
import scipy.io.wavfile as wav
import math
import struct
#import MLS.logic_layer.player as player
import matplotlib.pyplot as plot
from matplotlib.backends.backend_pdf import PdfPages

print "Type the path of the first .wav file to be plotted:"
filename1 = raw_input("")

print "Type the path of the second .wav file to be plotted:"
filename2 = raw_input("")

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

(samplerate1, data1) = readWavfile(filename1)
(samplerate2, data2) = readWavfile(filename2)

# #compute time vector
# time = len(data)/samplerate
# timevector = numpy.linspace(0, len(data), time*samplerate)
# print len(timevector), len(data)

#Normalize data
print "Do you want to normalize the data? y/n"
ans = raw_input("")

if ans == 'y':
    print "Normalizing..."
    data1 = numpy.divide(data1, float(max(data1)))
    data2 = numpy.divide(data2, float(max(data2)))
    print "Done normalizing..."
else:
    data1 = data1
    data2 = data2

print "Do you want to trim the length? y/n"
ans = raw_input("")
if ans == 'y':
    print "How much to keep in percentage? From 0-1"
    trim = raw_input()
    trim = float(trim)
    newlength1 = len(data1)*trim
    newlength2 = len(data2)*trim
    print "Trimming..."
    data1 = data1[:math.floor(newlength1)]
    data2 = data2[:math.floor(newlength2)]
    print "Done trimming..."
    print "Keeping the first", len(data1), "samples"
else:
    data1 = data1
    data2 = data2



print "Saving to pdf..."
fig = plot.figure(dpi=60)
F = plot.gcf()
Size = F.get_size_inches()
F.set_size_inches(8, 4)
plot.grid()
plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
plot.plot(data1)
plot.plot(data2)
plot.xlabel("Samples")
plot.ylabel("Amplitude")
pp = PdfPages(filename1+'.pdf')
pp.savefig(fig)
pp.close()
print "Done saving..."