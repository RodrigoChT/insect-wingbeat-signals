import os
import random as rd
import soundfile as sf

from wavs import Wavs

class Files:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.file_names = self.obtain_file_names()
        self.amount = len(self.file_names)

    def obtain_file_names(self):
        # grab all wav files inside the directory and subdirectories
        file_names = [os.path.join(root, name)
                      for root, dirs, files in os.walk(self.path)
                      for name in files
                      if name.endswith(('.wav'))]

        return file_names

    def obtain_wav_data(self,
                        frequency,
                        amount = 0,
                        random = False):
        # if no amount in chosen then grab all
        if amount == 0:
            amount = self.amount

        if random:
            selection = rd.sample(self.file_names, amount)
        else:
            selection = self.file_names[:amount]

        # read all files in the selection
        wav_data = Wavs([sf.read(file_name)[0]
                         for file_name in selection],
                        frequency,
                        self.amount)

        return wav_data

