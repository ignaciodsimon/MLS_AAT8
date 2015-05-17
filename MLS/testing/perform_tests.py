"""
Test script, used to validate the core functions.

Joe.
"""

import numpy
import wave
import matplotlib.pyplot as plot
from matplotlib.backends.backend_pdf import PdfPages

from MLS.logic_layer import generate_mls, compute_ir, player, measurement
# __package__ = "testing"

if __name__ == "__main__":

    # ---------------------------------
    #  PART 1 - TESTING MLS GENERATION
    # ---------------------------------

    # print "Generating MLS signals ..."
    # signal_order_3 = generate_mls.generateMLS(sequenceLength=pow(2, 3))
    # signal_order_7 = generate_mls.generateMLS(sequenceLength=pow(2, 7))
    # signal_order_15 = generate_mls.generateMLS(sequenceLength=pow(2, 15))
    #
    # print "Computing FFT of generated signals ..."
    # fft_order_3 = numpy.abs(numpy.fft.fft(signal_order_3, n=pow(2, 3)-1))
    # fft_order_7 = numpy.abs(numpy.fft.fft(signal_order_7, n=pow(2, 7)-1))
    # fft_order_15 = numpy.abs(numpy.fft.fft(signal_order_15, n=pow(2, 15)-1))
    #
    # print "Plotting results ..."
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(signal_order_7)
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("Waveform of a MLS(3) signal")
    # pp = PdfPages('waveform_mls_3.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
    # plot.stem(fft_order_3)
    # plot.xlabel("Frequency bins")
    # plot.ylabel("Amplitude")
    # plot.title("Module of spectrum of MLS(3)")
    # pp = PdfPages('fft_mls_order_3.pdf')
    # pp.savefig(fig)
    # pp.close()
    # print "Mean:", numpy.mean(signal_order_3) / pow(10, -3.0/20) * 100, "%"
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
    # plot.stem(fft_order_7)
    # plot.xlabel("Frequency bins")
    # plot.ylabel("Amplitude")
    # plot.title("Module of spectrum of MLS(7)")
    # pp = PdfPages('fft_mls_order_7.pdf')
    # pp.savefig(fig)
    # pp.close()
    # print "Mean:", numpy.mean(signal_order_7) / pow(10, -3.0/20) * 100, "%"
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(fft_order_15)
    # plot.xlabel("Frequency bins")
    # plot.ylabel("Amplitude")
    # plot.title("Module of spectrum of MLS(15)")
    # pp = PdfPages('fft_mls_order_15.pdf')
    # pp.savefig(fig)
    # pp.close()
    # print "Mean:", numpy.mean(signal_order_15) / pow(10, -3.0/20) * 100, "%"
    #
    # print "Done."

    # ---------------------------------
    #  PART 2 - TESTING IR COMPUTATION
    # ---------------------------------

    # inputSignal = signal_order_7
    # known_h = []
    #
    # print "Reading IR from file ..."
    # wf = wave.open("demo_IR.wav", "rb")
    # sampleFormat = wf.getsampwidth()    # 16 bit
    # channels = wf.getnchannels()        # 2 channels
    # sampleRate = wf.getframerate()      # 44100
    # framesPerBuffer = 1024              # chunk size
    # frames = wf.readframes(wf.getnframes())
    # known_h = player._convertStreamToChannel(frames)
    # known_h = known_h[250:425]
    # known_h = numpy.divide(known_h, float(max(known_h)))
    #
    # print "Generating output with convolution ..."
    # output = numpy.convolve(inputSignal, known_h)
    #
    # print "Estimating IR with circular x-corr ..."
    # input_padded = [0]*len(output)
    # input_padded[0:len(inputSignal)] = inputSignal
    # estimated_h = computeIR.computeCircularXCorr(output, input_padded)
    # estimated_h = numpy.divide(estimated_h, float(max(estimated_h)))
    # estimated_h = estimated_h[0:175]

    # print "Plotting results ..."
    # plot.subplot(4, 1, 1)
    # plot.plot(inputSignal)
    # plot.xlabel("Input signal")
    # plot.subplot(4, 1, 2)
    # plot.plot(known_h)
    # plot.xlabel("Known IR")
    # plot.subplot(4, 1, 3)
    # plot.plot(output)
    # plot.xlabel("Output")
    # plot.subplot(4, 1, 4)
    # plot.plot(estimated_h)
    # plot.xlabel("Estimated IR")
    # plot.show()

    # print "Saving plots to PDF ..."
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(inputSignal)
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("Input signal, MLS(7), to device under test")
    # pp = PdfPages('demo_ir_input_signal.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(known_h)
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("Known IR of simulated device under test")
    # pp = PdfPages('demo_ir_known_IR.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(output)
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("Output of the device under test")
    # pp = PdfPages('demo_ir_output.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(estimated_h)
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("Estimated IR of device under test, short MLS")
    # pp = PdfPages('demo_ir_estimated_IR.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # error = numpy.subtract(known_h, estimated_h)
    # error_RMS = computeIR._computeRMSValue(error)
    # print "[SHORT MLS] RMS value of error:", error_RMS, "- which represents:", error_RMS / max(estimated_h) * 100.0, "%"
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.12, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(error)
    # plot.axis([0, len(error), -0.2, 0.2])
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("Error in estimated IR of device under test, short MLS")
    # pp = PdfPages('demo_ir_error_IR.pdf')
    # pp.savefig(fig)
    # pp.close()


    # AGAIN BUT THIS TIME WITH ORDER 15
    # inputSignal = signal_order_15

    # print "Generating output with convolution ..."
    # output = numpy.convolve(inputSignal, known_h)
    #
    # print "Estimating IR with circular x-corr ..."
    # input_padded = [0]*len(output)
    # input_padded[0:len(inputSignal)] = inputSignal
    # estimated_h = computeIR.computeCircularXCorr(output, input_padded)
    # estimated_h = numpy.divide(estimated_h, float(max(estimated_h)))
    # estimated_h = estimated_h[0:len(known_h)]

    # print "Plotting results ..."
    # plot.subplot(4, 1, 1)
    # plot.plot(inputSignal)
    # plot.xlabel("Input signal")
    # plot.subplot(4, 1, 2)
    # plot.plot(known_h)
    # plot.xlabel("Known IR")
    # plot.subplot(4, 1, 3)
    # plot.plot(output)
    # plot.xlabel("Output")
    # plot.subplot(4, 1, 4)
    # plot.plot(estimated_h)
    # plot.xlabel("Estimated IR")
    # plot.show()

    # print "Saving plots to PDF ..."
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.09, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(estimated_h)
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("Estimated IR of device under test, using a higher order MLS signal")
    # pp = PdfPages('demo_ir_estimated_IR_high_order.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # error = numpy.subtract(known_h, estimated_h)
    # error_RMS = computeIR._computeRMSValue(error)
    # print "[LONG MLS] RMS value of error:", error_RMS, "- which represents:", error_RMS / max(estimated_h) * 100.0, "%"
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.12, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(error)
    # plot.axis([0, len(error), -0.2, 0.2])
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("Error in estimated IR of device under test, long MLS")
    # pp = PdfPages('demo_ir_error_IR_high_order.pdf')
    # pp.savefig(fig)
    # pp.close()

    # --------------------------------------
    #  PART 3 - TESTING SNR BY COMPENSATION
    # --------------------------------------

    # settings = measurement.MeasurementSettings()
    # settings.decayTime = 0.2
    # settings.signalAmplitude = 0.99
    # results = measurement.executeMeasurement(settings)
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.12, right=0.95, bottom=0.14, top=0.92)
    # plot.stem(results.computedImpulseResponse[0:20])
    # plot.axis([-0.5, 20, -0.1, 1.1])
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("Impulse response using both inputs in loop")
    # pp = PdfPages('ir_compensation_both_loop.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # ideal_IR = [0] * len(results.computedImpulseResponse)
    # ideal_IR[0] = 1
    # error = numpy.subtract(results.computedImpulseResponse, ideal_IR)
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.12, right=0.95, bottom=0.14, top=0.92)
    # plot.stem(error[0:20])
    # plot.axis([-0.5, 20, -0.1, 0.1])
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("Difference in IR using both inputs in loop to ideal delta function")
    # pp = PdfPages('ir_compensation_both_loop_error.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # error_dB = 20 * numpy.log10(computeIR._computeRMSValue(error))
    # equivalent_precision_bits = abs(error_dB) / 6
    # print "SNR of sound card:", error_dB, " - equivalent of having:", equivalent_precision_bits, "bits"

    # ----------------------------------
    #  PART 4 - TESTING LOOP COMPARISON
    # ----------------------------------

    # print "Reading IR from file ..."
    # wf = wave.open("loop1.wav", "rb")
    # sampleFormat = wf.getsampwidth()    # 16 bit
    # channels = wf.getnchannels()        # 2 channels
    # sampleRate = wf.getframerate()      # 44100
    # framesPerBuffer = 1024              # chunk size
    # frames = wf.readframes(wf.getnframes())
    # loop_melisa = player._convertStreamToChannel(frames)
    # loop_melisa = loop_melisa[0:20]
    # loop_melisa = numpy.divide(loop_melisa, float(max(loop_melisa)))
    #
    # wf = wave.open("loop_ads_tech.wav", "rb")
    # sampleFormat = wf.getsampwidth()    # 16 bit
    # channels = wf.getnchannels()        # 2 channels
    # sampleRate = wf.getframerate()      # 44100
    # framesPerBuffer = 1024              # chunk size
    # frames = wf.readframes(wf.getnframes())
    # loop_ads_tech = player._convertStreamToChannel(frames)
    # loop_ads_tech = loop_ads_tech[0:20]
    # loop_ads_tech = numpy.divide(loop_ads_tech, float(max(loop_ads_tech)))
    #
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.12, right=0.95, bottom=0.14, top=0.92)
    # plot.stem(loop_melisa)
    # plot.axis([-1, 20, -0.1, 1.1])
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("Commercial MLS system connected in loop")
    # pp = PdfPages('ir_comparison_melisa.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.12, right=0.95, bottom=0.14, top=0.92)
    # plot.stem(loop_ads_tech)
    # plot.axis([-1, 20, -0.1, 1.1])
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("Developed IR measuring system connected in loop")
    # pp = PdfPages('ir_comparison_our_system.pdf')
    # pp.savefig(fig)
    # pp.close()

    # --------------------------------------
    #  PART 5 - TESTING SNR BY COMPENSATION
    # --------------------------------------

    # measurementSettings = measurement.MeasurementSettings()
    # measurementSettings.decayTime = 5.0
    # measurementSettings.signalAmplitude = 0.99
    # measurementSettings.referenceSignalIsLeft = False
    #
    # measurementResults = measurement.executeMeasurement(measurementSettings)
    # measurementResults.computedImpulseResponse = numpy.divide(measurementResults.computedImpulseResponse,
    #                                                           max(numpy.abs(measurementResults.computedImpulseResponse)))
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.12, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(measurementResults.partialIR_Right)
    # # plot.axis([-1, 20, -0.1, 1.1])
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("IR of channel connected in loop")
    # pp = PdfPages('ir_loop_compensation_loop_channel.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.12, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(measurementResults.partialIR_Left)
    # # plot.axis([-1, 20, -0.1, 1.1])
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("IR of channel connected to device under test")
    # pp = PdfPages('ir_loop_compensation_measuring_channel.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.grid()
    # plot.subplots_adjust(left=0.12, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(measurementResults.computedImpulseResponse[0:15000])
    # # plot.axis([-1, 20, -0.1, 1.1])
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.title("IR of device under test with compensation applied")
    # pp = PdfPages('ir_loop_compensation_device_compensated.pdf')
    # pp.savefig(fig)
    # pp.close()

    # -----------------------------------------
    #  PART 6 - COMPARING WITH THE OLD MELISSA
    # -----------------------------------------

    # AKG-414 MICROPHONE

    # wf = wave.open("IR_comparison/melisa_414_chamber_1.wav", "rb")
    # sampleFormat = wf.getsampwidth()    # 16 bit
    # channels = wf.getnchannels()        # 2 channels
    # sampleRate = wf.getframerate()      # 44100
    # framesPerBuffer = 1024              # chunk size
    # frames = wf.readframes(wf.getnframes())
    # melisa_414 = player._convertStreamToChannel(frames)
    # melisa_414 = melisa_414[440:600]
    # melisa_414 = numpy.divide(melisa_414, float(max(melisa_414)))
    #
    # wf = wave.open("IR_comparison/oursystem_414_chamber_1.wav", "rb")
    # sampleFormat = wf.getsampwidth()    # 16 bit
    # channels = wf.getnchannels()        # 2 channels
    # sampleRate = wf.getframerate()      # 44100
    # framesPerBuffer = 1024              # chunk size
    # frames = wf.readframes(wf.getnframes())
    # oursystem_414 = player._convertStreamToChannel(frames)
    # oursystem_414 = oursystem_414[440-3:600-3]
    # oursystem_414 = numpy.divide(oursystem_414, float(max(oursystem_414)))
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.subplots_adjust(left=0.12, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(melisa_414, 'r')
    # plot.plot(oursystem_414, 'g')
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.grid()
    # plot.axis([1, 150, -2, 1.25])
    # plot.legend(["Commercial MLS system", "Developed software"])
    # plot.title("AKG-414 microphone IR measured with the two systems")
    # pp = PdfPages('ir_systems_comparison_akg_414.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # # ROOM
    #
    # wf = wave.open("IR_comparison/melisa_genIR10_room.wav", "rb")
    # sampleFormat = wf.getsampwidth()    # 16 bit
    # channels = wf.getnchannels()        # 2 channels
    # sampleRate = wf.getframerate()      # 44100
    # framesPerBuffer = 1024              # chunk size
    # frames = wf.readframes(wf.getnframes())
    # melisa_room = player._convertStreamToChannel(frames)
    # melisa_room = melisa_room[420:570]
    # melisa_room = numpy.divide(melisa_room, float(max(melisa_room)))
    #
    # wf = wave.open("IR_comparison/oursystem_genIR10_room.wav", "rb")
    # sampleFormat = wf.getsampwidth()    # 16 bit
    # channels = wf.getnchannels()        # 2 channels
    # sampleRate = wf.getframerate()      # 44100
    # framesPerBuffer = 1024              # chunk size
    # frames = wf.readframes(wf.getnframes())
    # oursystem_room = player._convertStreamToChannel(frames)
    # oursystem_room = oursystem_room[420-3:570-3]
    # oursystem_room = numpy.divide(oursystem_room, float(max(oursystem_room)))
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.subplots_adjust(left=0.12, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(melisa_room, 'r')
    # plot.plot(oursystem_room, 'g')
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.grid()
    # plot.axis([1, 150, -1.25, 1.25])
    # plot.legend(["Commercial MLS system", "Developed software"])
    # plot.title("Standard listening room IR measured with the two systems")
    # pp = PdfPages('ir_systems_comparison_room.pdf')
    # pp.savefig(fig)
    # pp.close()
    #
    # # SHURE SM-58
    #
    # wf = wave.open("IR_comparison/melisa_shure_chamber_1.wav", "rb")
    # sampleFormat = wf.getsampwidth()    # 16 bit
    # channels = wf.getnchannels()        # 2 channels
    # sampleRate = wf.getframerate()      # 44100
    # framesPerBuffer = 1024              # chunk size
    # frames = wf.readframes(wf.getnframes())
    # melisa_shure = player._convertStreamToChannel(frames)
    # melisa_shure = melisa_shure[440:540]
    # melisa_shure = numpy.divide(melisa_shure, float(max(melisa_shure)))
    #
    # wf = wave.open("IR_comparison/oursystem_shure_chamber_1.wav", "rb")
    # sampleFormat = wf.getsampwidth()    # 16 bit
    # channels = wf.getnchannels()        # 2 channels
    # sampleRate = wf.getframerate()      # 44100
    # framesPerBuffer = 1024              # chunk size
    # frames = wf.readframes(wf.getnframes())
    # oursystem_shure = player._convertStreamToChannel(frames)
    # oursystem_shure = oursystem_shure[440-3:540-3]
    # oursystem_shure = numpy.divide(oursystem_shure, float(max(oursystem_shure)))
    #
    # fig = plot.figure(dpi=60)
    # F = plot.gcf()
    # Size = F.get_size_inches()
    # F.set_size_inches(8, 4)
    # plot.subplots_adjust(left=0.12, right=0.95, bottom=0.14, top=0.92)
    # plot.plot(melisa_shure, 'r')
    # plot.plot(oursystem_shure, 'g')
    # plot.xlabel("Samples")
    # plot.ylabel("Amplitude")
    # plot.grid()
    # plot.axis([1, 100, -1.75, 1.25])
    # plot.legend(["Commercial MLS system", "Developed software"])
    # plot.title("Shure SM-58 microphone IR measured with the two systems")
    # pp = PdfPages('ir_systems_comparison_shure.pdf')
    # pp.savefig(fig)
    # pp.close()

    # ---------------------------------------
    #  PART 7 - TESTING THE COMPUTATION TIME
    # ---------------------------------------

    # import timeit
    # print "Testing MLS signal generation function ..."
    # amount_of_iterations = 100
    # _time_MLS = timeit.timeit("generate_mls.generateMLS(sequenceLength=pow(2, 15))",
    #                           setup="from MLS.logic_layer import generate_mls",
    #                           number=amount_of_iterations)
    # print "  time in seconds: ", _time_MLS / amount_of_iterations

    # print "Testing multitasking execution time difference ..."
    # from MLS.logic_layer import parallel_functions
    # import datetime
    #
    # number_of_iterations = 100
    # total_time = 0
    #
    # def dummyFunction1():
    #     time_started = datetime.datetime.now()
    #     return time_started
    #
    # def dummyFunction2():
    #     time_started = datetime.datetime.now()
    #     return time_started
    #
    # for _n in range(number_of_iterations):
    #     [time1, time2] = parallel_functions.runInParallel(function1=dummyFunction1, f1args=[], function2=dummyFunction2, f2args=[])
    #     total_time += (time2 - time1).total_seconds() * 1000
    #
    # delay = total_time / number_of_iterations
    # print "  difference in milliseconds:", delay
    # print "  which means a difference of ", delay / 1000 * 44100, "(samples)"

    print "That's all."