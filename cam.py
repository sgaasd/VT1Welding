import numpy as np
import cv2 as cv
import Microphones

#line 6-13 should be called before the loop starts
cap = cv.VideoCapture(1) ###should be 1 with an external webcam
# Define the codec and create VideoWriter object
#fourcc = cv.VideoWriter_fourcc(*'XVID')
#out = cv.VideoWriter('output.avi', fourcc, 20.0, (640,  480))
fourcc = cv.VideoWriter_fourcc(*"mp4v")
#fourcc = cv.VideoWriter_fourcc(*"h264")
out = cv.VideoWriter('output.mp4', fourcc, 20.0, (640,  480)) #('name', encoder, framerate, (resolution)) This should be adjusted to fit the camera
array=Microphones.CallMic(20,16000) #If microphones doesn't work check 9 in microphones to specify which device it uses. To get an overveiw of the devices look at the printed list ###THIS STARTS THE MICROPHONE RECORDING

##this is just for the counter 
close= False
close_counter=0


while close== False:
    ##this can be called at the start of the loop it will start showing the cam stream but wont save, which means you can adjust the camera
    ret, frame = cap.read()
    cv.waitKey(1)
    cv.imshow('frame', frame)
    if not ret:
        print("Can't receive frame")
        break

    ###### this should be called when we want to save data
    out.write(frame)## writes images to the file
    
    if  close_counter>1000:
        break


    close_counter=close_counter+1
# Release everything if job is finished
Microphones.stoprec(array)###STOP AUDIO RECORDING
cap.release()
out.release()
cv.destroyAllWindows()