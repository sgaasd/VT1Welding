import socket
import os
from datetime import datetime
import pandas as pd
import cv2 as cv
import Microphones

'''
Style guide comes from: 
https://google.github.io/styleguide/pyguide.html#3164-guidelines-derived-from-guidos-recommendations
'''

def save_data(test_type,data,rating):
    print("saving data")
    today= datetime.today()
    test_name=str(today.year)+str(today.month)+str(today.day)
    cur_dir = os.getcwd()
    number=len(os.listdir(cur_dir+"/Data/"+test_type))+1
    number=f"{number:03d}"
    test_name=str(test_name)+"_"+str(rating)+"_"+str(test_type)+"_"+str(number)+".csv"
    print(test_name)
    data.to_csv("Data/"+str(test_type)+"/"+test_name,index=False)

def list_range(start, end, step):
    lst=[start]
    for i in range(1,end):
        start=start+step
        lst.append(start)
    return lst

#MetafileIndhold(Typetest=T-joint, Størrelse=10mm, Dato=Day/month, Nummer=1, Link til dataen)
#DataNavn(Dato=Day/Month, Nummer=1)
#DataIndhold(time, Current, Voltage, WireFeeder, Velosity, Sound)

def data_exchange_with_cowelder():
    ur10_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = 50000
    ur10_socket.bind(('', PORT))
    ur10_socket.listen(1)
    connection, address = ur10_socket.accept()
    print(connection)
    print(address)

    close_socket = False
    initiate_weld_signal = "NULL"
    weldment_done = False

    cap = cv.VideoCapture(1)
    fourcc = cv.VideoWriter_fourcc(*"mp4v")
    today= datetime.today()
    cur_dir = os.getcwd()
    number=len(os.listdir(cur_dir+"/Data/cam"))+1
    test_name=str(today.year)+str(today.month)+str(today.day)
    test_name=str(test_name)+"_cam_"+str(number)+'.mp4'
    out = cv.VideoWriter('Data/cam/'+test_name, fourcc, 30.0, (1920, 1080))

    while close_socket == False:

        ret, frame = cap.read()
        cv.waitKey(1)
        cv.imshow('frame', frame)

        initiate_go_signal = input("Type 'start' to initiate program: ")
        welding_data_list = ["Current, Voltage, Wire-feed"]
        if initiate_go_signal == "start": #Start til før svejsning
            while initiate_weld_signal == "NULL":
                connection.send((bytes('(1)', 'ascii'))) #Sender signal til roboten om den skal starte
                recieved_data = connection.recv(1024) # forventer at modtaget et signal om at den er kørt til svejseposition
                if recieved_data.decode("utf-8") == 3:
                #if recieved_data == int.to_bytes(3,4,'big'):
                    welding_tip_in_position = True
                    initiate_weld_signal = input("Type 'weld' to start welding: ")
        if initiate_weld_signal == "weld" and welding_tip_in_position == True: #Start svejsning og begynder data indsamling
            initiate_go_signal = "NULL"
            Micdata=Microphones.CallMic(20,16000)
            connection.send((bytes('(2)', 'ascii')))
            
            while weldment_done == False: 
                recieved_data = connection.recv(1024)
                ret, frame = cap.read()
                cv.waitKey(1)
                cv.imshow('frame', frame)
                out.write(frame) #Start saving the frames to the video
                if recieved_data.decode("utf-8") == 4:
                #if recieved_data == int.to_bytes(4,4,'big'):
                    weldment_done = True  
                else:
                    welding_data_list.append(recieved_data.decode("utf-8"))
            welding_tip_in_position = False        
            initiate_weld_signal = "NULL"
            #print(welding_data_list)
        if weldment_done == True: #Gemmer data
            welding_data_dataframe = pd.DataFrame(welding_data_list)
            welding_data_dataframe = welding_data_dataframe[0].str.split(',',expand=True)
            new_header = welding_data_dataframe.iloc[0] #grab the first row for the headery
            welding_data_dataframe = welding_data_dataframe[1:] #take the data less the header row
            welding_data_dataframe.columns = new_header #set the header row as the welding_data_dataframe header
            Hz=10
            lst=list_range(0,len(welding_data_dataframe.index),1/Hz)
            welding_data_dataframe['time [s]']=lst

            cols =  welding_data_dataframe.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            welding_data_dataframe = welding_data_dataframe[cols]

            #print(welding_data_dataframe)
            Micdata=Microphones.stoprec(Micdata)
            mic_df=pd.DataFrame(Micdata,columns=['Channel_1','Channel_2','Channel_3','Channel_4'])
            Hz=16000
            lst=list_range(0,len(mic_df.index),1/Hz)
            mic_df['time [s]']=lst
            cols =  mic_df.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            mic_df = mic_df[cols]
            out.release()

            save_data(test_type="weld", data=welding_data_dataframe, rating=1)
            save_data(test_type="mic", data=mic_df, rating=1)
            weldment_done = False

        if input("Continue to weld another piece press 'y' | shutdown press 'n': ") == "y":
            close_socket = True
            connection.send((bytes('(5)', 'ascii')))
            connection.close()
            cap.release()
            cv.destroyAllWindows()
        else:
            pass


def main():
    data_exchange_with_cowelder()

if __name__ == '__main__':
    main()