    
import socket
import os
from datetime import datetime
import numpy as np
import pandas as pd
import struct

def savedata(testtype,data,rating):
    print("saving data")
    today= datetime.today()
    testname=str(today.year)+str(today.month)+str(today.day)
    curdir = os.getcwd()
    number=len(os.listdir(curdir+"\Data\weld"))+1
    number=f"{number:03d}"
    testname=str(testname)+"_"+str(rating)+"_"+str(testtype)+"_"+str(number)+".csv"
    print(testname)
    data.to_csv("Data/weld/"+testname,index=False)
    #np.savetxt("Data/"+str(testtype)+"/"+testname,data,delimiter=",")

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
signal2 = "t"
weldment = "NotDone"
while close == False:
    signal = input("press y to go to start position: ")
    if signal == "y": #Start til før svejsning
        while signal2 == "t":
            conn.send((bytes('(1)', 'ascii'))) #Sender signal til roboten om den skal starte
            data = conn.recv(16) # forventer at modtaget et signal om at den er kørt til svejseposition
            print(data)
            print(type(data))
            if data == int.to_bytes(3,4,'big'):
                readyToWeld = True
                start = False
                datalist = ["Current, Voltage, Wire-feed"]
                signal2 = input("press n to go to start position: ")
    if signal2 == "n" and readyToWeld == True: #Start svejsning og begynder data indsamling
        signal = "not y"
        while weldment == "NotDone": 
            conn.send((bytes('(2)', 'ascii')))
            data = conn.recv(1024)
            if data == int.to_bytes(4,4,'big'):
                weldment = "Done"
                readyToWeld = False
            else:
                datalist.append(data.decode("utf-8"))
                
        signal2 = "t"
        print(datalist)
    if weldment == "Done": #Gemmer data
        df = pd.DataFrame(datalist)
        df = df[0].str.split(',',expand=True)
        new_header = df.iloc[0] #grab the first row for the headery
        df = df[1:] #take the data less the header row
        df.columns = new_header #set the header row as the df header
        print(df)
        savedata(testtype="weld", data=df, rating=1)
        weldment ="NotDone"
    else:
        pass

    #if closeSocket == True:
    #    close == True


conn.close()



