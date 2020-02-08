import scipy.signal as sig
import pandas as pd
import random as rd
import matplotlib.pyplot as plt
import os
import math
import numpy as np
import itertools

class Freqs:
    def __init__(self,
                 power,
                 freqs,
                 amount):
        self.power = power
        self.freqs = freqs
        self.amount = amount

    def find_freq_peaks(self, prop_max):
        """Find number of peaks that have at least 'prop_max'% power"""
        peaks_index = [sig.find_peaks(obs,
                                      height = max(obs) / prop_max)[0]
                      for obs in self.power]
        return Peaks(peaks_index, self.freqs)

    # def filter_by(self, key):
    #     """Filter data by 'key'"""
    #     filtered_data = Freqs(self.data[key])
    #     return filtered_data
    #
    # # todo: store plots in better resolution
    # def plot(self,
    #          num_plots = 20,
    #          random = False,
    #          save = False,
    #          file_name = 'temp',
    #          show = True):
    #     """Plot frequencies in multiples of 10 observations"""
    #     if random:
    #         selection = rd.sample(range(self.amount), num_plots)
    #     else:
    #         selection = range(num_plots)
    #
    #     for i in range(len(selection)):
    #         plt.subplot(math.ceil(num_plots/10), 10, i + 1)
    #         plt.plot(self.freqs[selection[i]]['freq'],
    #                  self.freqs[selection[i]]['power'])
    #
    #     if save:
    #         full_file_name = os.path.join('./plots', file_name + '.png')
    #         if os.path.exists(full_file_name):
    #             raise ValueError('File name for plot already exists.')
    #         else:
    #            plt.savefig(full_file_name)
    #
    #     if show:
    #         plt.show()

class Peaks:
    def __init__(self,
                 peaks_index,
                 freqs):
        self.peaks_index = peaks_index
        self.amount = len(self.peaks_index)
        self.freqs = freqs

    def check_if_in_range(self, freq_range):
        """Do the frequency peaks include the relevant frequency range?"""
        results = np.empty(self.amount, bool)
        for i in range(self.amount):
            a = freq_range[0] <= self.freqs[self.peaks_index[i]]
            b = self.freqs[self.peaks_index[i]] <= freq_range[1]
            results[i] = any(a&b)
        return results

    def check_if_max_amount(self, max_amount):
        num_peaks = np.asarray([len(obs) for obs in self.peaks_index])
        results = num_peaks > max_amount
        return  results

    # todo: check that one of the deleted ones is not the main one
    # todo: do not jump from x1 to x3?
    # todo: exclude peaks of very low frequencies
    def ignore_peak_harmonics(self, precision):
        """Remove peaks that are harmonics of the first 2 peaks"""
        results = []
        for i in range(self.amount):
            obs = self.freqs[self.peaks_index[i]]
            print(obs)
            main_fqs = []
            for j in range(2):
                main_fqs = main_fqs + [obs[0]]
                harmonics = (obs / obs[0]) % 1 # see how close they are multiples
                harmonics = [min(a, 1 - a) < precision for a in harmonics] 
                #harmonics = [not abs(har - 1 for har in harmonics]  # todo: relax demand
                obs = list(itertools.compress(obs, harmonics))
                if len(obs) == 0:
                    break
            main_fqs = main_fqs + obs
            main_fqs.sort()
            results.append(main_fqs)
        print(results)
        return results

    def filter_by(self, key):
        """Filter data by 'key'"""
        filtered_peaks_index = list(itertools.compress(self.peaks_index, key))
        return Peaks(filtered_peaks_index, self.freqs)
