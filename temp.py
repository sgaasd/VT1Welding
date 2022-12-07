import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
fs, data = wavfile.read('channel_1.wav') # load the data
a = data.T[0] # this is a two channel soundtrack, I get the first track
b=a # this is 8-bit track, b is now normalized on [-1,1)
c = fft(data) # calculate fourier transform (complex numbers list)
d = len(data)/2  # you only need half of the fft list (real signal symmetry)
plt.plot(abs(c[:]),'r') 
plt.show()