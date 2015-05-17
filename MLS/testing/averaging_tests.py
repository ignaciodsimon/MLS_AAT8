'''
This script is designed to test the effect of noise in the recordings, and how does that affect the estimation of the
associated impulse response. It is vital for discerning whether the averaging must be done pre or post circular cross
correlation, and if the code for estimating the IR is correct or not.

The problem comes from the fact that the performed operation should be linear, thus it should not matter when the
averaging is performed, but in the conducted experiments, it shows that computing it before increases the noise and
computing it after reduces the noise.

 Conclusion notes:
-------------------

With "correctIR...":

    This method corrects the module / phase of both signals

    Averaging helps reducing noise, and the result does not change whether it's pre- or post-averaging

    clean:          -41.10
    no avg:         -19.21
    pre avg:        -29.25
    post avg:       -29.25
    improvement:    -10.05


With "XCorr..."

    This method multiplies the complex spectrum of both signals

    Averaging does not seem to help at all, but because it seems that it's
    way too perfect always and since it can not be improved ...

    clean:          -20.97
    no avg:         -19.22
    pre avg:        -20.83
    post avg:       -20.83
    improvement:    -1.6


It seems that the process of estimating the IR is linear since averaging results in the same using pre or post
averaging

Joe.
'''


from MLS.logic_layer import compute_ir
from MLS.logic_layer import generate_mls
from MLS.data_layer import wav_files_handling
import random
import numpy
import matplotlib.pyplot as plot
from matplotlib.backends.backend_pdf import PdfPages

# ir_method = 'XCorr'
ir_method = 'Compensate'


def computeIR(signalA, signalB):

    if ir_method == 'XCorr':
        computed_ir = compute_ir.computeCircularXCorr(signalA, signalB, frequencyBinsFactor=1)

    if ir_method == 'Compensate':
        computed_ir = compute_ir.correctSignalWithIR(signalA, signalB)

    computed_ir = numpy.divide(computed_ir, numpy.max(numpy.abs(computed_ir)))
    return computed_ir


# Reading the known IR from file
read_wav_file = wav_files_handling.readWavImpulseResponseFile('demo_IR.wav', normalize=True)
known_IR = read_wav_file.impulseResponse[0:10000]
# plot.plot(known_IR)
# plot.show()

# Generating the excitation signal (MLS)
excitation_signal = generate_mls.generateMLS()

# Creating the additive noises with zero mean
random.seed(0)
noise_amplitude = 0.3
noise_1 = numpy.random.normal(0, noise_amplitude, len(excitation_signal))
noise_2 = numpy.random.normal(0, noise_amplitude, len(excitation_signal))
noise_3 = numpy.random.normal(0, noise_amplitude, len(excitation_signal))
noise_4 = numpy.random.normal(0, noise_amplitude, len(excitation_signal))
noise_5 = numpy.random.normal(0, noise_amplitude, len(excitation_signal))
noise_6 = numpy.random.normal(0, noise_amplitude, len(excitation_signal))
noise_7 = numpy.random.normal(0, noise_amplitude, len(excitation_signal))
noise_8 = numpy.random.normal(0, noise_amplitude, len(excitation_signal))


# spect_before = 20 * numpy.log10(numpy.abs((numpy.fft.fft(noise_1))))
# plot.semilogx(spect_before)
# plot.grid()
# plot.show()

# # Adding an additional component to make it non-white
# tone_signal = [0.2 * numpy.sin(2 * numpy.pi * 1000 * n / 44100 + numpy.random.random()/1000) for n in range(len(noise_1))]
# noise_1 = numpy.add(noise_1, tone_signal)
# tone_signal = [0.2 * numpy.sin(2 * numpy.pi * 1000 * n / 44100 + numpy.random.random()/1000) for n in range(len(noise_1))]
# noise_2 = numpy.add(noise_2, tone_signal)
# tone_signal = [0.2 * numpy.sin(2 * numpy.pi * 1000 * n / 44100 + numpy.random.random()/1000) for n in range(len(noise_1))]
# noise_3 = numpy.add(noise_3, tone_signal)
# tone_signal = [0.2 * numpy.sin(2 * numpy.pi * 1000 * n / 44100 + numpy.random.random()/1000) for n in range(len(noise_1))]
# noise_4 = numpy.add(noise_4, tone_signal)
# tone_signal = [0.2 * numpy.sin(2 * numpy.pi * 1000 * n / 44100 + numpy.random.random()/1000) for n in range(len(noise_1))]
# noise_5 = numpy.add(noise_5, tone_signal)
# tone_signal = [0.2 * numpy.sin(2 * numpy.pi * 1000 * n / 44100 + numpy.random.random()/1000) for n in range(len(noise_1))]
# noise_6 = numpy.add(noise_6, tone_signal)
# tone_signal = [0.2 * numpy.sin(2 * numpy.pi * 1000 * n / 44100 + numpy.random.random()/1000) for n in range(len(noise_1))]
# noise_7 = numpy.add(noise_7, tone_signal)
# tone_signal = [0.2 * numpy.sin(2 * numpy.pi * 1000 * n / 44100 + numpy.random.random()/1000) for n in range(len(noise_1))]
# noise_8 = numpy.add(noise_8, tone_signal)

# spect_after = 20 * numpy.log10(numpy.abs((numpy.fft.fft(noise_1))))
# plot.semilogx(spect_after)
# plot.grid()
# plot.show()
# # plot.plot(noise_1)
# # plot.show()


noise_1 = numpy.subtract(noise_1, numpy.mean(noise_1))
noise_2 = numpy.subtract(noise_2, numpy.mean(noise_2))
noise_3 = numpy.subtract(noise_3, numpy.mean(noise_3))
noise_4 = numpy.subtract(noise_4, numpy.mean(noise_4))
noise_5 = numpy.subtract(noise_5, numpy.mean(noise_5))
noise_6 = numpy.subtract(noise_6, numpy.mean(noise_6))
noise_7 = numpy.subtract(noise_7, numpy.mean(noise_7))
noise_8 = numpy.subtract(noise_8, numpy.mean(noise_8))

# Creating inputs with noise
noisy_input_1 = excitation_signal + noise_1
noisy_input_2 = excitation_signal + noise_2
noisy_input_3 = excitation_signal + noise_3
noisy_input_4 = excitation_signal + noise_4
noisy_input_5 = excitation_signal + noise_5
noisy_input_6 = excitation_signal + noise_6
noisy_input_7 = excitation_signal + noise_7
noisy_input_8 = excitation_signal + noise_8

# Generating the outputs of the "virtual device"
clean_output = numpy.convolve(excitation_signal, known_IR)
noisy_output_1 = numpy.convolve(noisy_input_1, known_IR)
noisy_output_2 = numpy.convolve(noisy_input_2, known_IR)
noisy_output_3 = numpy.convolve(noisy_input_3, known_IR)
noisy_output_4 = numpy.convolve(noisy_input_4, known_IR)
noisy_output_5 = numpy.convolve(noisy_input_5, known_IR)
noisy_output_6 = numpy.convolve(noisy_input_6, known_IR)
noisy_output_7 = numpy.convolve(noisy_input_7, known_IR)
noisy_output_8 = numpy.convolve(noisy_input_8, known_IR)

# Estimating impulse responses
estimated_h_clean = computeIR(clean_output, excitation_signal)
estimated_h_noise_1 = computeIR(noisy_output_1, excitation_signal)
estimated_h_noise_2 = computeIR(noisy_output_2, excitation_signal)
estimated_h_noise_3 = computeIR(noisy_output_3, excitation_signal)
estimated_h_noise_4 = computeIR(noisy_output_4, excitation_signal)
estimated_h_noise_5 = computeIR(noisy_output_5, excitation_signal)
estimated_h_noise_6 = computeIR(noisy_output_6, excitation_signal)
estimated_h_noise_7 = computeIR(noisy_output_7, excitation_signal)
estimated_h_noise_8 = computeIR(noisy_output_8, excitation_signal)

# Trimming estimated impulse responses
trimming_point = len(known_IR)
estimated_h_clean = estimated_h_clean[0:trimming_point]
estimated_h_noise_1 = estimated_h_noise_1[0:trimming_point]
estimated_h_noise_2 = estimated_h_noise_2[0:trimming_point]
estimated_h_noise_3 = estimated_h_noise_3[0:trimming_point]
estimated_h_noise_4 = estimated_h_noise_4[0:trimming_point]
estimated_h_noise_5 = estimated_h_noise_5[0:trimming_point]
estimated_h_noise_6 = estimated_h_noise_6[0:trimming_point]
estimated_h_noise_7 = estimated_h_noise_7[0:trimming_point]
estimated_h_noise_8 = estimated_h_noise_8[0:trimming_point]

# Creating the pre-averaging version
pre_averaged_output = numpy.divide(noisy_output_1 + noisy_output_2 + noisy_output_3 + noisy_output_4 +
                                   noisy_output_5 + noisy_output_6 + noisy_output_7 + noisy_output_8, 8)
estimated_h_pre_average = computeIR(pre_averaged_output, excitation_signal)
estimated_h_pre_average = estimated_h_pre_average[0:trimming_point]

# Creating the post-averaging version
estimated_h_post_average = numpy.divide(estimated_h_noise_1 + estimated_h_noise_2 +
                                        estimated_h_noise_3 + estimated_h_noise_4 +
                                        estimated_h_noise_5 + estimated_h_noise_6 +
                                        estimated_h_noise_7 + estimated_h_noise_8, 8)

# Computing the error for all cases
error_clean = numpy.subtract(estimated_h_clean, known_IR)
error_noisy = numpy.subtract(estimated_h_noise_7, known_IR)
error_pre_averaging = numpy.subtract(estimated_h_pre_average, known_IR)
error_post_averaging = numpy.subtract(estimated_h_post_average, known_IR)

# # Plotting the errors
# dynamic_range_to_show = 0.02
# plot.plot(error_clean[0:270], 'g')
# plot.plot(numpy.add(error_noisy[0:270], 0.008), 'r')
# plot.plot(numpy.add(error_pre_averaging[0:270], -0.008), 'b')
# plot.plot(numpy.add(error_post_averaging[0:270], -2*0.008), 'y')
# plot.axis([0, 270, - dynamic_range_to_show, dynamic_range_to_show])
# plot.legend(['Error clean processing', 'Error noisy - no averaging',
#              'Error noisy - pre averaging', 'Error noisy - post averaging'])
# plot.show()

# RMS of error:
rms_error_clean = 20*numpy.log10(numpy.sqrt(numpy.sum(numpy.dot(error_clean[0:230], error_clean[0:230]))))
rms_error_noisy = 20*numpy.log10(numpy.sqrt(numpy.sum(numpy.dot(error_noisy[0:230], error_noisy[0:230]))))
rms_error_pre_averaging = 20*numpy.log10(numpy.sqrt(numpy.sum(numpy.dot(error_pre_averaging[0:230],
                                                                        error_pre_averaging[0:230]))))
rms_error_post_averaging = 20*numpy.log10(numpy.sqrt(numpy.sum(numpy.dot(error_post_averaging[0:230],
                                                                         error_post_averaging[0:230]))))

print 'Clean process: ', rms_error_clean
print 'No averaging process: ', rms_error_noisy
print 'Pre process: ', rms_error_pre_averaging
print 'Post process: ', rms_error_post_averaging
print 'Improvement: ', rms_error_post_averaging - rms_error_noisy
print 'Improvement (db/double)', (rms_error_post_averaging - rms_error_noisy) / 8

# Plotting the impulse responses
fig = plot.figure(dpi=60)
F = plot.gcf()
Size = F.get_size_inches()
F.set_size_inches(8, 4)
dynamic_range_to_show = 0.07
plot.plot(known_IR[0:260], 'g')
plot.plot(numpy.add(estimated_h_noise_2[0:260], 0.025), 'y')
plot.plot(numpy.add(estimated_h_pre_average[0:260], -0.025), 'r')
plot.plot(numpy.add(estimated_h_post_average[0:260], -2*0.025), 'b')
plot.axis([0, 260, - dynamic_range_to_show, dynamic_range_to_show])
plot.legend(['Known IR', 'No averaging', 'Pre averaging', 'Post averaging'])
plot.grid()
plot.xlabel('Samples')
plot.ylabel('Amplitude')
plot.title('Comparison of pre / post averaging with white noise')
plot.show()
pp = PdfPages('pre-post-demonstration.pdf')
pp.savefig(fig)
pp.close()