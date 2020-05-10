import scipy.signal as sig
import math
import numpy as np

from freqs import Freqs

class Wavs:
    def __init__(self, raw, frequency, amount):
        self.wav_raw = raw
        self.frequency = frequency
        self.amount = amount

    def downsample(self, obj_frequency):
        """Downsample orginial data down to the 'obj_frequency'"""
        self.wav_raw = [sig.decimate(wav,
                                     math.floor(self.frequency / obj_frequency))
                        for wav in self.wav_raw]
        self.frequency = obj_frequency
        
    def filter_data(self,
                    lowcut,
                    highcut,
                    order):
        """Apply a 4th order Butterworth filter"""
        nyq = 0.5 * self.frequency
        low = lowcut / nyq
        high = highcut / nyq
        b, a = sig.butter(order, [low, high], btype='band')
        self.wav_filtered = [sig.lfilter(b, a, wav)
                         for wav in self.wav_raw]

    def perform_PSD(self):
        """Performn a Power Spectral Decomposition"""
        freq_data = [sig.welch(wav, self.frequency)
                     for wav in self.wav_filtered]

        # Check that frequencies buckets are the same across the data
        if self.amount > 1:
            all_equal = True
            for i in range(1, self.amount):
                all_equal = all_equal & np.array_equal(freq_data[i - 1][0],
                                                       freq_data[i][0])
                if all_equal == False:
                    raise ValueError('Not all files have the same frequency buckets.')

        freq_data_ins = Freqs([obs[1] for obs in freq_data],
                              freq_data[0][0],
                              self.amount)
        return freq_data_ins