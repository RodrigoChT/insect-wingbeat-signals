import scipy.signal as sig
import pandas as pd
import math

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

    def perform_fourier_transform(self):
        """Performn a Fourier Transform"""
        freq_data = [sig.welch(wav, self.frequency)
                     for wav in self.wav_filtered]
        freq_data = Freqs([pd.DataFrame(data = dict(freq = obs[0],
                                                    power = obs[1]))
                           for obs in freq_data],
                          self.amount)
        return freq_data