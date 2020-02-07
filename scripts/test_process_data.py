from files import Files
from freqs import Peaks
a = Files('test', '/home/rodrigo/Documents/data/Wingbeats/Ae. aegypti')
b = a.obtain_wav_data(8000, 3)
b.filter_data(75,1000,5)
c = b.perform_fourier_transform()
peaks = c.find_freq_peaks(10)
filt1 = peaks.check_if_in_range([500, 600])
peaks1 = peaks.filter_by(filt1)
filt2 = peaks1.check_if_max_amount(2)
peaks2 = peaks.filter_by(filt2)
#print(peaks.peaks_index)
#print(peaks1.peaks_index)
#print(peaks2.peaks_index)

peaks.ignore_peak_harmonics(3)
#c.plot(num_plots=30, save = True, file_name='test2', show=False)
