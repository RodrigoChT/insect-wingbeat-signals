# import packages
from os import listdir, walk
from os.path import isfile, join
from itertools import compress
import matplotlib.pyplot as plt
import statistics as stats

import soundfile as sf
import scipy.signal as sig
import numpy as np

# global parameters
ae_aegypti_path = '/home/rodrigo/Documents/data/Wingbeats/Ae. aegypti'
data_path = '/home/rodrigo/Documents/data/Wingbeats'

# todo allow more depth than 1 directory
# # number of obs per species
# for i in listdir(data_path):
#     directories = [join(data_path, i, dir) for dir in listdir(i)]
#     wav_files = []
#     for j in directories:
#         wav_files.append(join(j, file) for file in lisdir(j))
#     print(i)
#     print(length(wav_files))

# read 1 single file
#wavdata_single, a = sf.read('..\data\Wingbeats\Ae. aegypti\D_16_12_12_19_46_13\F161212_195751_255_G_050.wav')

# read Ae. aegypti data
ae_aegypti_directories = [join(ae_aegypti_path,
                               dir) for dir in listdir(ae_aegypti_path)]
wav_files = []
for dir_i in ae_aegypti_directories:
    wav_files = wav_files + \
                [join(dir_i, file) for file in listdir(dir_i)
                 if isfile(join(dir_i, file))]

[join(root, name)
 for root, dirs, files in walk(path)
 for name in files
 if name.endswith(('.wav'))]


# wav_files = [join(ae_aegypti_directories[0],
#                   file) for file in listdir(ae_aegypti_directories[0])]

wav_data = [sf.read(file_name)[0] for file_name in wav_files]

# plot 25 wave files
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.plot(wav_data[i])
plt.show()


#### Cleaning data
# 4th order Butterworth filter (IIR ?)
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = sig.butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = sig.lfilter(b, a, data)
    return y

# Plot FT for a subset of data
j = 0
for i in range(0, 15, 3):
    plt.subplot(5, 3, i + 1)
    plt.plot(wav_data[j])

    plt.subplot(5, 3, i + 2)
    b = butter_bandpass_filter(wav_data[j],
                               75,
                               1000,
                               8000,
                               4)
    plt.plot(b)

    plt.subplot(5, 3, i + 3)
    c, d = sig.welch(b,
                     8000  # is overlap 50% by default here?
                     )
    plt.plot(c, d,
             'r')

    j += 1
plt.show()

# Plot FT for even more data
for i in range(50):
    plt.subplot(5, 10, i + 1)
    c, d = sig.welch(butter_bandpass_filter(wav_data[i],
                                            75,
                                            1000,
                                            8000,
                                            4),
                     8000)
    plt.plot(c, d)

plt.show()

# convert all data to frequency domain
fq_data = [sig.welch(butter_bandpass_filter(single_wav,
                                            75,
                                            1000,
                                            8000,
                                            4),
                     8000)
           for single_wav in wav_data]

# find peaks in frequency data
#z = sig.find_peaks_cwt(fq_data[30][1], 200/30+np.zeros(129))
peak_min_height = max(fq_data[30][1])/10
z = sig.find_peaks(fq_data[30][1], height = peak_min_height) #todo: smarter way of selecting peaks
plt.plot(fq_data[30][0], fq_data[30][1])
plt.plot(fq_data[30][0][z[0]], fq_data[30][1][z[0]], '*')

def find_peaks_values(fq_data, prop_max):
    fq_peaks = [sig.find_peaks(single_fq[1],
                               height = max(single_fq[1])/prop_max)
                for single_fq in fq_data]
    return fq_peaks

fq_peaks = find_peaks_values(fq_data, 10)

# find data with many more than 3 peaks
num_peaks = np.asarray([len(single_fq[0]) for single_fq in fq_peaks])
prob_signals_idx = num_peaks > 3
fq_data_prob = list(compress(fq_data, prob_signals_idx))
fq_peaks_prob = list(compress(fq_peaks, prob_signals_idx))

# plot data with more than 3 peaks
for i in range(50):
    plt.subplot(5, 10, i + 1)
    plt.plot(fq_data_prob[i][0], fq_data_prob[i][1])
    plt.plot(fq_data_prob[i][0][fq_peaks_prob[i][0]],
             fq_data_prob[i][1][fq_peaks_prob[i][0]], '*')

plt.show()

# do not count harmonics
# todo: only look for harmonics of important frequencies
def not_harmonics(fq_peaks_prob):
    result = []
    for i in range(len(fq_peaks_prob)):
        single_fq = fq_peaks_prob[i][0]
        main_fqs = []
        for j in range(2):
            main_fqs = main_fqs + [single_fq[0]]
            harmonics = single_fq / single_fq[0] # dividing by bins not exact freq
            harmonics = [not i.is_integer() for i in harmonics] # todo: relax demand
            single_fq = list(compress(single_fq, harmonics))
            if len(single_fq) == 0:
                break
        main_fqs = main_fqs + single_fq
        main_fqs.sort()
        result.append(main_fqs)
    return result

# find data with more than 3 peaks (not counting harmonics)
fq_peaks_prob_2 = not_harmonics(fq_peaks_prob)
num_peaks_2 = np.asarray([len(single_fq) for single_fq in fq_peaks_prob_2])
prob_signals_idx_2 = num_peaks_2 > 3
fq_data_prob_2 = list(compress(fq_data_prob, prob_signals_idx_2))
fq_peaks_prob_2 = list(compress(fq_peaks_prob_2, prob_signals_idx_2))


for i in range(50):
    plt.subplot(5, 10, i + 1)
    plt.plot(fq_data_prob[i][0], fq_data_prob[i][1])
    plt.plot(fq_data_prob[i][0][fq_peaks_prob_2[i]],
             fq_data_prob[i][1][fq_peaks_prob_2[i]], '*')

plt.show()