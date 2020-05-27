import os
import pandas as pd
from pathlib import Path
import numpy as np
import itertools

from files import Files

#### Parameters
# file paths
insect_dirs_path = '' # directory that contains 1 directory per insect species. The wav files can be arranged in lower
                      # directories that can be shared with other file types.
plots_path = '' # single directory where all the plots will be stored
results_path = '' # single directory where the lists of selected and discarded wav file names will be stored

# processing settings
amount_per_insect = 0 # how many wav files to process per species, 0 will grab all available data
num_plots = 200 # how many plots to draw per species, 0 will draw no plots
random_files_plotted = False # if True, then a random subset of signals plots will be drawn. If False, the first set
                             # of signals will be drawn
max_peaks = 3 # max amount of peaks to still consider valid observation (3 for flies, 4 for mosquitoes)
freq_range = [160, 600] # valid frequency rate (160-600 for flies, 400-1000 for mosquitoes)
record_freq = 8000 # record frequency
freq_filter = [75, 1000] # range of Butterworth passband filter

#### Script

# Extract insect names
insect_names = os.listdir(insect_dirs_path)
number_species = len(insect_names)

# Prepare output lists
total = []
selected = []
discarded = []

# for each insect species...
for i in range(number_species):
    files = Files(insect_names[i],
                  os.path.join(insect_dirs_path, insect_names[i]))

    # load wav files
    wavs = files.obtain_wav_data(record_freq, amount_per_insect)

    # total observations per insect species
    total.append(wavs.amount)

    # filter out unimportant frequencies
    wavs.filter_data(freq_filter[0], freq_filter[1], 5)

    # PSD
    freqs = wavs.perform_PSD()

    # calculate frequency peaks
    peaks = freqs.find_freq_peaks(10)

    # ignore harmonic peaks
    peaks_ignoring_harm = peaks.ignore_peak_harmonics(0.4, 160)

    # find samples with no peaks in range
    idx_in_range = peaks.check_if_in_range(freq_range)

    # find samples with 3 or more peaks
    idx_3_peaks_ignoring_harm = peaks_ignoring_harm.check_if_max_amount(max_peaks)

    # find samples with high background power
    idx_high_background, prob_obs = freqs.check_if_background_is_high(0.05)
    freqs_high_background = freqs.filter_by(idx_high_background)
    freqs_low_background = freqs.filter_by(idx_high_background, invert=True)

    # separate clean from muddled signals
    discard_filter = (idx_high_background | idx_3_peaks_ignoring_harm) | np.invert(idx_in_range)
    freq_selected = freqs.filter_by(discard_filter, invert=True)
    freq_discarded = freqs.filter_by(discard_filter)

    peaks_selected = peaks_ignoring_harm.filter_by(discard_filter, invert=True)
    peaks_discarded = peaks_ignoring_harm.filter_by(discard_filter)

    selected.append(freq_selected.amount)
    discarded.append(freq_discarded.amount)

    # store plots
    if num_plots > 0:

        # draw and store plots
        freq_selected.plot(insect_names[i] + '_selected',
                           plots_path,
                           total_num_plots=num_plots,
                           save=True,
                           show=False,
                           random=random_files_plotted)

        freq_discarded.plot(insect_names[i] + '_discarded',
                            plots_path,
                            total_num_plots=num_plots,
                            save=True,
                            show=False,
                            random=random_files_plotted)

    # store what files were selected and discarded
    Path(results_path).mkdir(parents=True, exist_ok=True)
    selected_files = list(itertools.compress(files.file_names, np.invert(discard_filter)))
    with open(os.path.join(results_path, insect_names[i] + '_selected.txt'), 'w') as f:
        for item in selected_files:
            f.write("%s\n" % item)

    discarded_files = list(itertools.compress(files.file_names, discard_filter))
    with open(os.path.join(results_path, insect_names[i] + '_discarded.txt'), 'w') as f:
        for item in discarded_files:
            f.write("%s\n" % item)

# show and store results
results = pd.DataFrame({'species': insect_names,
                        'total': total,
                        'selected': selected,
                        'discarded': discarded})

print(results)
results.to_csv(os.path.join(results_path, 'selected_obs_summary.csv'),
               index=False)
