import matplotlib.pyplot as plt
from files import Files

a = Files('test', '/home/pi/insect_wingbeat_signals/recordings/tests')
b = a.obtain_wav_data(frequency = 44100)
#b.downsample(8000)
#b.filter_data(75,1000,5)
b.wav_filtered = b.wav_raw

#plt.plot(b.wav_filtered[0])
#plt.show()

c = b.perform_fourier_transform()
plt.plot(c.freqs[0]['freq'],
         c.freqs[0]['power'])
plt.show()

#c.plot(num_plots=2, save = False, show=True)