from files import Files
a = Files('test', '/home/rodrigo/Documents/data/Wingbeats/Ae. aegypti')
b = a.obtain_wav_data(50)
b.filter_data(75,1000,5)
c = b.perform_fourier_transform()
print(c.freqs[1])
c.plot(num_plots=30, save = True, file_name='test2', show=False)
