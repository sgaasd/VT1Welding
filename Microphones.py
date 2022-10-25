from multiprocessing.connection import wait
import sounddevice as sd
from scipy.io.wavfile import write
def CallMic(seconds,fs):
   # fs = 44100  # Sample rate
    # seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    
    write('output.wav', fs, myrecording)  # Save as WAV file 

CallMic(3,44100)

def startmic(fs):
    myrecording = sd.rec(samplerate=fs, channels=2)

    wait(5)

    sd.stop()
    write('output2.wav', fs, myrecording) 

startmic(44100)











