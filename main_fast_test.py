import socket
import os
from datetime import datetime
import pandas as pd
import cv2 as cv
import time
import numpy as np

'''
Style guide comes from: 
https://google.github.io/styleguide/pyguide.html#3164-guidelines-derived-from-guidos-recommendations
'''
#Saves and names a data frame based on the type and a rating of the weldment
def save_data(data_type,data,rating):
    print("saving data")
    today= datetime.today()
    test_name=str(today.year)+str(today.month)+str(today.day)
    cur_dir = os.getcwd()
    number=len(os.listdir(cur_dir+"/Data/"+data_type))+1
    number=f"{number:03d}"
    test_name=str(test_name)+"_"+str(rating)+"_"+str(data_type)+"_"+str(number)+".csv"
    print(test_name)
    data.to_csv("Data/"+str(data_type)+"/"+test_name,index=False)
    return "Data/"+str(data_type)+"/"+test_name


#function that controls communication with the robot and starts and stops any recordings
def data_exchange_with_cowelder():
    current,voltage,wirefeed,gas_flow,t_horizontal,t_vertical,discribtion=0,0,0,0,0,0,0
    df_last_setting=0
    Hz_sound=16000
    Hz_weld=500
    PORT = 50000
    SAMPLERATE = 10
    ur10_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ur10_socket.bind(('', PORT))
    ur10_socket.listen(1)
    connection, address = ur10_socket.accept()
    print(connection)
    print(address)

    close_socket = False
    initiate_weld_signal = "NULL"
    weldment_done = False
    initiate = True

    
    

    while close_socket == False:
        if initiate == True:
            initiate = False

        initiate_go_signal = input("Type 'start' to initiate program: ")
        welding_data_list = ["Current, Voltage, Wire-feed, Gas-flow"] ###SKAL DETTE ÆNDRES????
        if initiate_go_signal == "start": #Start til før svejsning
            while initiate_weld_signal == "NULL":
                connection.send((bytes('(1)', 'ascii'))) #Sender signal til roboten om den skal starte
                recieved_data = connection.recv(1024) # forventer at modtaget et signal om at den er kørt til svejseposition
                #if recieved_data.decode("utf-8") == 3:
                if recieved_data == int.to_bytes(3,4,'big'):
                    welding_tip_in_position = True
                    initiate_weld_signal = input("Type 'weld' to start welding: ")
        if initiate_weld_signal == "weld" and welding_tip_in_position == True: #Start svejsning og begynder data indsamling
            initiate_go_signal = "NULL"
            connection.send((bytes('(2)', 'ascii')))
            unix_time_start=datetime.now()
            unix_time_start=time.mktime(unix_time_start.timetuple())*1e3 + unix_time_start.microsecond/1e3

            while weldment_done == False: 
                connection.send((bytes('(2)', 'ascii')))
                recieved_data = connection.recv(1024)
                if recieved_data == int.to_bytes(4,4,'big'):
                    connection.send((bytes('(0)', 'ascii')))
                    unix_time_end=datetime.now()
                    unix_time_end=time.mktime(unix_time_end.timetuple())*1e3 + unix_time_end.microsecond/1e3
                    weldment_done = True  

                else:
                    #welding_data_list.append(recieved_data.decode("utf-8"))
                    welding_data_list.append(recieved_data.decode("utf-8"))
                    #print("welding data saved")
            welding_tip_in_position = False        
            initiate_weld_signal = "NULL"
            #print(welding_data_list)
        if weldment_done == True: #Gemmer data
            welding_data_dataframe = pd.DataFrame(welding_data_list)
            welding_data_dataframe = welding_data_dataframe[0].str.split(',',expand=True)
            new_header = welding_data_dataframe.iloc[0] #grab the first row for the headery
            welding_data_dataframe = welding_data_dataframe[1:] #take the data less the header row
            welding_data_dataframe.columns = new_header #set the header row as the welding_data_dataframe header
            lst=np.linspace(unix_time_start,unix_time_end,len(welding_data_dataframe.index))
            welding_data_dataframe['time [s]']=lst
            cols =  welding_data_dataframe.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            welding_data_dataframe = welding_data_dataframe[cols]


            weldment_done = False

        if input("Continue to weld another piece press 'y' | shutdown press 'n': ") == "n":
            close_socket = True
            connection.send((bytes('(5)', 'ascii')))
            connection.close()
            cv.destroyAllWindows()
        else:
            initiate = True



def main():
    data_exchange_with_cowelder()


if __name__ == '__main__':
    main()