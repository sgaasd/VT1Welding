from multiprocessing.connection import wait
import sounddevice as sd
from scipy.io.wavfile import write
import time
import numpy as np

list=sd.query_devices() ###use this to find the microphone
print(list)

def CallMic(seconds,fs):
   # fs = 44100  # Sample rate
    # seconds = 3  # Duration of recording
    sd.default.device=17,6 # Channels(0 is processed data, 1-4 raw data, 5 is playback data)
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=6)
    #sd.wait()  # Wait until recording is finished
    write('output.wav', fs, myrecording) 
    #write('channel_1.wav', fs, myrecording[:,1])  # Save as WAV file 
    return myrecording

#array=CallMic(10,16000)

def stoprec(array):
    sd.stop()
    print(array)
    
    #np.savetxt("raw.csv", array, delimiter=",")

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


    #print (datastop)

    cutarray=array[0:len(array[:,0])-datastop,:]
    cutarray = cutarray[:,1:5]
    write('channel_1.wav', 16000, cutarray[:,1])
    write('output.wav', 16000, cutarray) 
    #np.savetxt("cut.csv", cutarray, delimiter=",")
    return cutarray


if __name__ == '__main__':
    array=CallMic(20,16000)
    time.sleep(5)
    stoprec(array)











