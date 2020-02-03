import scipy.signal as sig
import pandas as pd
import random as rd
import matplotlib.pyplot as plt
import os

class Freqs:
    def __init__(self, freqs, amount):
        self.freqs = freqs
        self.amount = amount

    def find_freq_peaks(self, prop_max):
        """Find number of peaks that have at least 'prop_max'% power"""
        freq_peaks = [sig.find_peaks(obs['power'],
                                     height = max(obs['power']) / prop_max)
                      for obs in self.freqs]
        return freq_peaks

    def filter(self, key):
        """Filter data by 'key'"""
        filtered_data = Freqs(self.data[key])
        return filtered_data

    # todo: store plots in better resolution
    def plot(self,
             num_plots = 20,
             random = False,
             save = False,
             file_name = 'temp',
             show = True):
        """Plot frequencies in multiples of 10 observations"""
        if random:
            selection = rd.sample(range(self.amount), num_plots)
        else:
            selection = range(num_plots)

        for i in range(len(selection)):
            plt.subplot(num_plots/10, 10, i + 1)
            plt.plot(self.freqs[selection[i]]['freq'],
                     self.freqs[selection[i]]['power'])

        if save:
            full_file_name = os.path.join('./plots', file_name + '.png')
            if os.path.exists(full_file_name):
                raise ValueError('File name for plot already exists.')
            else:
               plt.savefig(full_file_name)

        if show:
            plt.show()

