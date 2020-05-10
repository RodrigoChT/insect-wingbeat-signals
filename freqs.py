import scipy.signal as sig
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

    def check_if_background_is_high(self, prop_max):
        """Check if the average value of the PSD is equal or greater than prop_max*highest peak"""
        results = np.empty(self.amount, bool)
        prop_obs = np.empty(self.amount, float)

        for i in range(self.amount):
            power = self.power[i]
            max_power_idx = np.argmax(power)
            max_power = power[max_power_idx]
            mean_power = np.mean(np.delete(power, range(max(max_power_idx - 2, 0), max_power_idx + 3)))
            results[i] = mean_power >= prop_max*max_power
            prop_obs[i] = mean_power/max_power

        return results, prop_obs


    def filter_by(self, key, invert = False):
        """Filter data by 'key'"""
        if invert:
            key = np.invert(key)
        filtered_data = list(itertools.compress(self.power, key))

        return Freqs(filtered_data,
                     self.freqs,
                     len(filtered_data))

    def plot(self,
             file_name,
             plot_path,
             total_num_plots = 20,
             random = False,
             save = False,
             show = True,
             peaks = None):
        """Plot frequencies in multiples of 10 observations"""
        total_num_plots = min(total_num_plots, self.amount)

        if total_num_plots > 0:

            idx_2000hz = np.argmin(abs(self.freqs - 2000))
            max_plots = 50
            c = 0

            if random:
                total_selection = rd.sample(range(self.amount), total_num_plots)
            else:
                total_selection = range(total_num_plots)

            while True:

                num_plots = min(total_num_plots, max_plots)
                total_num_plots -= num_plots
                selection = total_selection[c * max_plots:min((c + 1) * max_plots,
                                                              len(total_selection))]

                num_rows = math.ceil(num_plots / 10)
                num_cols = 10
                fig, ax = plt.subplots(num_rows,
                                       num_cols,
                                       figsize=(25, 15))
                i = 0

                if num_rows > 1:
                    for row in ax:
                        for col in row:
                            if i < len(selection):
                                col.plot(self.freqs[0:idx_2000hz],
                                         self.power[selection[i]][0:idx_2000hz])
                                if peaks is not None:
                                    x = peaks.freqs[peaks.peaks_index[selection[i]]]
                                    y = self.power[selection[i]][peaks.peaks_index[selection[i]]]
                                    col.plot(x,
                                             y,
                                             '*')
                                    for a, b in zip(x, y):
                                        col.annotate(str(a), xy=(a, b))
                            i += 1
                else:
                    for row in ax:
                        if i < len(selection):
                            row.plot(self.freqs[0:idx_2000hz],
                                     self.power[selection[i]][0:idx_2000hz])
                            if peaks is not None:
                                x = peaks.freqs[peaks.peaks_index[i]]
                                y = self.power[selection[i]][peaks.peaks_index[i]]
                                row.plot(x,
                                         y,
                                         '*')
                                for a, b in zip(x, y):
                                    row.annotate(str(a), xy=(a, b))
                        i += 1

                if save:
                    full_file_name = os.path.join(plot_path, file_name + '_' + str(c) + '.png')
                    fig.savefig(full_file_name, dpi = 500, bbox_inches='tight')

                if show:
                    plt.show()

                if total_num_plots < 1:
                    break

                plt.close()
                c += 1

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
        results = num_peaks >= max_amount

        return  results

    def ignore_peak_harmonics(self, precision, floor_cutoff = 0):
        """Remove peaks that are harmonics of the first 2 peaks.
        'precision' = [0 to 1] with 0 being exact multiples.
        'floor_cutoff' determines the minimum peak to consider."""
        peaks = []

        for i in range(self.amount):
            obs = self.freqs[self.peaks_index[i]]
            obs_considered_idx = [i >= floor_cutoff for i in obs]
            main_fqs = list(itertools.compress(obs, np.invert(obs_considered_idx)))
            obs = list(itertools.compress(obs, obs_considered_idx))

            for j in range(min(2, len(obs))):
                main_fqs = main_fqs + [obs[0]]
                harmonics = (obs / obs[0]) % 1 # see how close they are multiples
                harmonics = [not(min(a, 1 - a) <= precision) for a in harmonics]
                obs = list(itertools.compress(obs, harmonics))

                if len(obs) == 0:
                    break

            main_fqs = main_fqs + obs
            main_fqs.sort()
            main_fqs = np.in1d(self.freqs, main_fqs)
            peaks.append(np.nonzero(main_fqs)[0])

        return Peaks(peaks, self.freqs)

    def filter_by(self, key, invert = False):
        """Filter data by 'key'"""
        if invert:
            key = np.invert(key)
        filtered_peaks_index = list(itertools.compress(self.peaks_index, key))

        return Peaks(filtered_peaks_index, self.freqs)
