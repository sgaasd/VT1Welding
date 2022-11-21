from multiprocessing.connection import wait
import sounddevice as sd
from scipy.io.wavfile import write
import time
import numpy as np

list=sd.query_devices()
print(list)
sd.default.device=14,4
def CallMic(seconds,fs):
   # fs = 44100  # Sample rate
    # seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=6)

    write('output.wav', fs, myrecording)  # Save as WAV file 
    return myrecording

array=CallMic(10,16000)

def stoprec(array):
    sd.stop()
    print(array)

    np.savetxt("raw.csv", array, delimiter=",")

    print(len(array[0,:]))
    datastop=0
    for i in range(0,len(array[0,:])-1):
        arrayflipped=np.flip(array[:,i],0)
        datastoptemp=np.nonzero(arrayflipped)
        datastoptemp=np.array(datastoptemp[0])
        if datastop==0:
            datastop=datastoptemp[0]
        elif datastoptemp[0]<datastop:
            datastop=datastoptemp[0]


    print (datastop)

    cutarray=array[0:len(array[:,0])-datastop,:]


    np.savetxt("cut.csv", cutarray, delimiter=",")
    return cutarray













