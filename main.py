import socket
import os
from datetime import datetime
import pandas as pd
import cv2 as cv
import Microphones
import time


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
    return "Data/"+str(test_type)+"/"+test_name

def list_range(start, end, step):
    lst=[start]
    for i in range(1,end):
        start=start+step
        lst.append(start)
    return lst

def tocontinue():
    while True:
        input_var=input("If you are ready to continue type \"y\": ")
        if input_var =="y":
            print("\n")

        else:
            print("You have to choose yes or no by typing \"y\" or \"n\" \n")
        
        break


current,voltage,wirefeed,gas_flow,t_horizontal,t_vertical,discribtion=0,0,0,0,0,0,0
df_last_setting=0
def meta_data(current,voltage,wirefeed,gas_flow,t_horizontal,t_vertical,discribtion,df):
    if t_horizontal==0:
        input_var="y"
    else:
        print(df)
        input_var=input("Do you want to change any of the current settings \"y\" or \"n\":")
    if input_var =="y":
        print("\n")
        #current
        no_answer=True
        while no_answer == True:
            input_var=input("What is the current input on the welding machine [A]: ")
            try:
                current = float(input_var)

                print(current)
                no_answer=False
            except ValueError:
                print('The provided value is not an float try again')
            print("\n")
        #voltage
        no_answer=True
        while no_answer == True:
            input_var=input("What is the voltage input on the welding machine [V]: ")
            try:
                voltage = float(input_var)

                print(voltage)
                no_answer=False
            except ValueError:
                print('The provided value is not an float try again')
            print("\n")
        #wirefeed
        no_answer=True
        while no_answer == True:
            input_var=input("What is the wire feed speed [mm/min]: ")
            try:
                wirefeed = float(input_var)

                print(wirefeed)
                no_answer=False
            except ValueError:
                print('The provided value is not an float try again')
            print("\n")
        #gas
        no_answer=True
        while no_answer == True:
            input_var=input("What is the gas flow [L/min]: ")
            try:
                gas_flow = float(input_var)

                print(gas_flow)
                no_answer=False
            except ValueError:
                print('The provided value is not an float try again')
            print("\n")
        
        no_answer=True
        while no_answer == True:
            input_var=input("What is the thickness of the horizontal parent material in mm: ")
            try:
                t_horizontal = float(input_var)

                print(t_horizontal)
                no_answer=False
            except ValueError:
                print('The provided value is not an float try again')
            print("\n")
        
        no_answer=True
        while no_answer == True:
            input_var=input("What is the thickness of the vertical parent material in mm: ")
            try:
                t_vertical = float(input_var)

                print(t_vertical)
                no_answer=False
            except ValueError:
                print('The provided value is not an float try again')
            print("\n")
        
        no_answer=True
        while no_answer == True:
            discribtion=input("Describtion of experiment: ")
            print("Your describtion was: " + discribtion)
            print("\n")
            input_var=input("Confirm if correct or try again by typing \"y\" or \"n\":")
            if input_var =="y":
                print("\n")
                no_answer=False
            elif input_var =="n":
                print("\n")
                print("Then try again")
        return current,voltage,wirefeed,gas_flow,t_horizontal,t_vertical,discribtion
    elif input_var =="n":
        print("\n")
        return current,voltage,wirefeed,gas_flow,t_horizontal,t_vertical,discribtion
        
        




        

def comment_data():
    no_answer=True
    while no_answer == True:
        input_var=input("Did the weld pass as a class c weldment\"y\" or \"n\":")
        if input_var =="y":
            print("\n")
            test_result=1
            no_answer=False
        elif input_var =="n":
            print("\n")
            test_result=0
            no_answer=False
        else:
            print("\n")
            print("You have to choose yes or no by typing \"y\" or \"n\" \n")

    no_answer=True
    while no_answer == True:
        notes=input("Notes after experiment (remember to write why it did or didn't pass): ")
        print("Your notes where: " + notes)
        print("\n")
        input_var=input("Confirm if correct or try again by typing \"y\" or \"n\":")
        if input_var =="y":
            print("\n")
            no_answer=False
        elif input_var =="n":
            print("\n")
            print("Then try again")

    
    return test_result,notes
#save_meta(t_horizontal,t_vertical,discribtion,test_result,notes):
def save_meta(test_nb,start_t,sample_rate_weld,sample_rate_sound,test_result,path_sound,path_weld,path_video,t_horizontal,t_vertical,current,voltage,wirefeed,gas_flow,discribtion,notes):
    today= datetime.today()
    test_name=str(today.year)+str(today.month)+str(today.day)
    list_of_inf=[[test_nb,test_name,start_t,sample_rate_weld,sample_rate_sound,test_result,path_sound,path_weld,path_video,t_horizontal,t_vertical,current,voltage,wirefeed,gas_flow,discribtion,notes]]
    df_of_inf=pd.DataFrame(list_of_inf,columns=['Test_number','Date_y_m_d','Start_time_[unix_ms]','Sample_rate_weld[Hz]','Sample_rate_sound[Hz]','Rating','Path_sound','Path_weld','Path_video','Thickness_hor[mm]','Thickness_ver[mm]','Current[A*10]','Voltage[V*10]','Wire_feed[m/min]','Gas_flow[L/min]','Describtion','Notes'])
    

    data_dir="Data/"
    data_type=["cam/","meta/","scan/","sound/","weld/"]

    cur_dir=os.listdir(data_dir+data_type[1])
    ##might have to be commentet out first time
    df = pd.read_csv("Data/meta/meta.csv", sep=",")

    df_param=pd.read_csv("Data/meta/semi_constant_param.csv",sep=',')
    df_of_inf = pd.concat([df_of_inf, df_param], ignore_index=True, sort=False)

    #this also has to be commentet out
    df = df.append(df_of_inf, ignore_index = True)
    print("saving data")
    
    cur_dir = os.getcwd()
    number=len(os.listdir(cur_dir+"/Data/meta"))+1
    number=f"{number:03d}"
    test_name=str(test_name)+"_"+str(test_result)+"_meta_"+str(number)+".csv"
    print(test_name)
    df.to_csv("Data/meta/meta.csv",index=False)
    return df_of_inf

#MetafileIndhold(Typetest=T-joint, Størrelse=10mm, Dato=Day/month, Nummer=1, Link til dataen)
#DataNavn(Dato=Day/Month, Nummer=1)
#DataIndhold(time, Current, Voltage, WireFeeder, Velosity, Sound)

def data_exchange_with_cowelder():
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
            cap = cv.VideoCapture(1)
            fourcc = cv.VideoWriter_fourcc(*"mp4v")
            today= datetime.today()
            cur_dir = os.getcwd()
            number=len(os.listdir(cur_dir+"/Data/cam"))+1
            test_name=str(today.year)+str(today.month)+str(today.day)
            test_name=str(test_name)+"_cam_"+str(number)+'.mp4'
            ret = cap.set(cv.CAP_PROP_FRAME_WIDTH,1920)
            ret = cap.set(cv.CAP_PROP_FRAME_HEIGHT,1080)
            out = cv.VideoWriter('Data/cam/'+test_name, fourcc, 30.0, (1920, 1080))
            path_video='Data/cam/'+test_name
            initiate = False
            #ret, frame = cap.read()
#        cv.waitKey(1)start
#        cv.imshow('frame', frame)

        initiate_go_signal = input("Type 'start' to initiate program: ")
        welding_data_list = ["Current, Voltage, Wire-feed"]
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
            Micdata=Microphones.CallMic(60,16000)
            connection.send((bytes('(2)', 'ascii')))
            unix_time=datetime.now()
            unix_time=time.mktime(unix_time.timetuple()) + unix_time.microsecond/1e3

            while weldment_done == False: 
                print("while loop")
                connection.send((bytes('(2)', 'ascii')))
                recieved_data = connection.recv(1024)
                print(recieved_data)
                ret, frame = cap.read()
#                cv.waitKey(1)
#                cv.imshow('frame', frame)
                out.write(frame) #Start saving the frames to the video
                #if recieved_data.decode("utf-8") == 4:
                if recieved_data == int.to_bytes(4,4,'big'):
                    connection.send((bytes('(0)', 'ascii')))
                    weldment_done = True  
                else:
                    #welding_data_list.append(recieved_data.decode("utf-8"))
                    welding_data_list.append(recieved_data.decode("utf-8"))
                    print("welding data saved")
            welding_tip_in_position = False        
            initiate_weld_signal = "NULL"
            #print(welding_data_list)
        if weldment_done == True: #Gemmer data
            welding_data_dataframe = pd.DataFrame(welding_data_list)
            welding_data_dataframe = welding_data_dataframe[0].str.split(',',expand=True)
            new_header = welding_data_dataframe.iloc[0] #grab the first row for the headery
            welding_data_dataframe = welding_data_dataframe[1:] #take the data less the header row
            welding_data_dataframe.columns = new_header #set the header row as the welding_data_dataframe header
            Hz_weld=100
            lst=list_range(unix_time,len(welding_data_dataframe.index),1/Hz_weld)
            welding_data_dataframe['time [s]']=lst

            cols =  welding_data_dataframe.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            welding_data_dataframe = welding_data_dataframe[cols]

            #print(welding_data_dataframe)
            Micdata=Microphones.stoprec(Micdata)
            mic_df=pd.DataFrame(Micdata,columns=['Channel_1','Channel_2','Channel_3','Channel_4'])
            Hz_sound=16000
            lst=list_range(unix_time,len(mic_df.index),1/Hz_sound)
            mic_df['time [s]']=lst
            cols =  mic_df.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            mic_df = mic_df[cols]
            out.release()

            path_weld=save_data(test_type="weld", data=welding_data_dataframe, rating=1)
            path_sound=save_data(test_type="sound", data=mic_df, rating=1)
            weldment_done = False

        if input("Continue to weld another piece press 'y' | shutdown press 'n': ") == "n":
            close_socket = True
            connection.send((bytes('(5)', 'ascii')))
            connection.close()
            cap.release()
            cv.destroyAllWindows()
        else:
            initiate = True
            cap.release()


def main():
    data_exchange_with_cowelder()

if __name__ == '__main__':
    #main()
    current,voltage,wirefeed,gas_flow,t_horizontal,t_vertical,discribtion=meta_data(current,voltage,wirefeed,gas_flow,t_horizontal,t_vertical,discribtion,df_last_setting)
    test_result,notes=comment_data()
    cur_dir = os.getcwd()
    number=len(os.listdir(cur_dir+"/Data/cam"))+1

    df_last_settings=save_meta(number,unix_time,Hz_weld,Hz_sound,test_result,path_sound,path_weld,path_video,t_horizontal,t_vertical,current,voltage,wirefeed,gas_flow,discribtion,notes)
