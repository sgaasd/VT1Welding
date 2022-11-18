    
import socket
import os
from datetime import datetime
import numpy as np


def savedata(testtype,data,rating):
    print("saving data")
    today= datetime.today()
    testname=str(today.year)+str(today.month)+str(today.day)
    curdir = os.getcwd()
    number=len(os.listdir(curdir+"\Data\weld"))+1
    number=f"{number:03d}"
    testname=str(testname)+"_"+str(rating)+"_"+str(testtype)+"_"+str(number)+".csv"
    print(testname)
    np.savetxt("Data/"+str(testtype)+"/"+testname,data,delimiter=",")

#MetafileIndhold(Typetest=T-joint, Størrelse=10mm, Dato=Day/month, Nummer=1, Link til dataen)
#DataNavn(Dato=Day/Month, Nummer=1)
#DataIndhold(time, Current, Voltage, WireFeeder, Velosity, Sound)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 50000))
s.listen(1)
conn, addr = s.accept()

print(conn)
print(addr)


close = False

while close == False:
    if start: #Start til før svejsning
        conn.send((bytes('(1)', 'ascii'))) #Sender signal til roboten om den skal starte
        data = conn.recv(16) # forventer at modtaget et signal om at den er kørt til svejseposition
        if data == "(readyToWeld)":
            readyToWeld = True
            start = False
            datalist = ["Current, Voltage, Wire-feed"]
            
    if startSvejsning and readyToWeld: #Start svejsning og begynder data indsamling
        conn.send((bytes('(2)', 'ascii')))
        data = conn.recv(16)
        datalist.append(data)
        if conn.recv(16) == "weldment_Done":
            weldment = "Done"

    if weldment == "Done": #Gemmer data
        savedata(testtype="weld", data=datalist, rating=1)
        weldment =="NotDone"

    if closeSocket == True:
        close == True


conn.close()



