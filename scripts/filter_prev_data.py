from files import Files
from freqs import Peaks

# select insect species
files = Files('test', '/home/rodrigo/Documents/data/Wingbeats/Ae. aegypti')
print(files.amount)

# load all files
wavs = files.obtain_wav_data(8000, 20000)

# filter out unimportant frequencies
wavs.filter_data(75,1000,5)

# Fourier transformation
freqs = wavs.perform_fourier_transform()

# calculate frequency peaks
peaks = freqs.find_freq_peaks(10)

# find samples with no peaks in range
idx_in_range = peaks.check_if_in_range([400, 900])
freqs_in_range = freqs.filter_by(idx_in_range, True)
#freqs_in_range.plot()

# find samples with more than 10 peaks
idx_more_4 = peaks.check_if_max_amount(4)
freq_more_4 = freqs.filter_by(idx_more_4)

# peaks1 = peaks.filter_by(filt1)
# filt2 = peaks1.check_if_max_amount(2)
# peaks2 = peaks.filter_by(filt2)
# #print(peaks.peaks_index)
# #print(peaks1.peaks_index)
# #print(peaks2.peaks_index)
#
# peaks_non_harm = peaks.ignore_peak_harmonics(0)
# peaks_non_harm_greater_1 = peaks_non_harm.check_if_max_amount(1)
# peaks_filt_non_harm = peaks_non_harm.filter_by(peaks_non_harm_greater_1)
# freqs_filt_non_harm = c.filter_by(peaks_non_harm_greater_1)
#
# print(peaks_non_harm_greater_1)
# print(freqs_filt_non_harm.amount)
#c.plot(num_plots=30, save = True, file_name='test2', show=False)
