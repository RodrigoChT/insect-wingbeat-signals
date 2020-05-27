# Insect wingbeat signals

This repository includes functionality for loading, reading, transforming, and evaluating insect wingbeat datasets (`Python 3.7.6`).
The script `scripts/filter_data.py` process wingbeat signals and separates them between valid and invalid observations based on a set of simple rules.

## How to use

1. Install the requirements listed in `requirements.txt`.

2. Organize the `wav` files such that all samples from each species are contained in a separate directory (they can be arranged in any manner inside it, including being divided into more directories) and that all of them are contained in a main directory. See the following example:

```
main_directory
|
└───species 1
│   │   species_1_wav01.wav
│   │   species_1_wav02.wav
│   │   ...
|   |
└───species 2
│   │   species_2_wav01.wav
│   │   species_2_wav02.wav
│   │   ...
|   |
└───...
|   |
```

3. Set the following mandatory parameters at the start of the script:
  * `insect_dirs_path` = path pointing to the `main_directory` shown above.
  * `plots_path` = path pointing to the directory where you want to store the generated plots.
  * `results_path` = path pointing to the directory where you want to store the lists of selected and discarded `wav` files.

4. If necessary, other parameters can be tweaked to process a specific amount of signals, change the thresholds for the selection rules, specify the frequency of the recordings, etc.

5. Check the generated plots for a visual comparison between a sample of the selected and the discarded signals per species. To improve the results you can tweak the parameters at the start of the script or add/remove selection rules.

6. For each species the files `speciesName_discarded.txt` and `speciesName_selected.txt` are generated and stored in `results_path`. They each include the full paths for all discarded and selected wingbeat signals, respectively. A file called `selected_obs_summary.csv` is also generated, it contains a table that details the total amount of files per species and how many were discarded and selected.
