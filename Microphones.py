from multiprocessing.connection import wait
import sounddevice as sd
from scipy.io.wavfile import write
import time
import numpy as np

list=sd.query_devices() ###use this to find the microphone
print(list)

#start microphone input: record time and frequency
def CallMic(seconds,fs):
    sd.default.device=17,6 # Channels(0 is processed data, 1-4 raw data, 5 is playback data)
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=6)

    write('output.wav', fs, myrecording) 
    return myrecording


#stop the microphonerecording prematurely and cuts the rest which would just be 0 when stoped early
def stoprec(array):
    sd.stop()
    print(array)
    
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


    cutarray=array[0:len(array[:,0])-datastop,:]
    cutarray = cutarray[:,1:5]
    write('channel_1.wav', 16000, cutarray[:,1])
    write('output.wav', 16000, cutarray) 
    return cutarray


if __name__ == '__main__':
    array=CallMic(60,16000)
    time.sleep(60)
    stoprec(array)











