import numpy as np
import cv2 as cv
import Microphones

cap = cv.VideoCapture(1)
# Define the codec and create VideoWriter object
#fourcc = cv.VideoWriter_fourcc(*'XVID')
#out = cv.VideoWriter('output.avi', fourcc, 20.0, (640,  480))

#fourcc = cv.VideoWriter_fourcc(*"mp4v")
fourcc = cv.VideoWriter_fourcc(*"h264")
out = cv.VideoWriter('output.mp4', fourcc, 20.0, (640,  480))

array=Microphones.CallMic(20,16000)
close= False
close_counter=0
while close== False:
    ret, frame = cap.read()
    cv.waitKey(1)
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame = cv.flip(frame, 0)
    # write the flipped frame
    out.write(frame)
    cv.imshow('frame', frame)
    if  close_counter>1000:
        break
    close_counter=close_counter+1
# Release everything if job is finished
Microphones.stoprec(array)
cap.release()
out.release()
cv.destroyAllWindows()