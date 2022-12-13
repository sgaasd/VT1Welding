from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

samplerate, data = wavfile.read('channel_1.wav')
datalist = data.tolist()
print(len(datalist))
plt.plot(datalist)
plt.show()

from scipy.fft import fft, fftfreq

# Number of samples in normalized_tone
N = samplerate * 4

yf = fft(data)
xf = fftfreq(N, 1 / samplerate)

plt.plot(xf, np.abs(yf))
plt.show()