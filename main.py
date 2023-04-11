import socket
import os
from datetime import datetime
import pandas as pd
import cv2 as cv
import Microphones
import time
import numpy as np
from threading import Thread

'''
Style guide comes from: 
https://google.github.io/styleguide/pyguide.html#3164-guidelines-derived-from-guidos-recommendations
'''

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=1):
        self.stream = cv.VideoCapture(src)
        self.ret = self.stream.set(cv.CAP_PROP_FRAME_WIDTH,1920)
        self.ret = self.stream.set(cv.CAP_PROP_FRAME_HEIGHT,1080)
        fourcc = cv.VideoWriter_fourcc(*"mp4v")
        today= datetime.today()
        cur_dir = os.getcwd()
        number=len(os.listdir(cur_dir+"/Data/cam"))+1
        test_name=str(today.year)+str(today.month)+str(today.day)
        test_name=str(test_name)+"_cam_"+str(number)+'.mp4'
        self.out = cv.VideoWriter('Data/cam/'+test_name, fourcc, 30.0, (1920, 1080))
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

        

    def initialise(self):
        pass

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

                self.out.write(self.frame) #Start saving the frames to the video

    def stop(self):
        self.stopped = True
        self.out.release()
        self.stream.release()
        cv.destroyAllWindows()
        
    def stop_camera(self):
        pass



#Saves and names a data frame based on the type and a rating of the weldment
def save_data(data_type,data,rating):
    print("saving data")
    today= datetime.today()
    test_name=today.strftime('%Y%m%d')
    cur_dir = os.getcwd()
    number=len(os.listdir(cur_dir+"/Data/"+data_type))+1
    number=f"{number:03d}"
    test_name=str(test_name)+"_"+str(rating)+"_"+str(data_type)+"_"+str(number)+".csv"
    print(test_name)
    data.to_csv("Data/"+str(data_type)+"/"+test_name,index=False)
    return "Data/"+str(data_type)+"/"+test_name

#simple function to pause the program until the user is rady to continue
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
#function for inputting the metadata that cant be collected automatically,
#  and also where a describtion of the test can be written
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
        
        




        
#For after the test is done to do the rating and for any notes observed
def comment_data():
    no_answer=True
    while no_answer == True:
        input_var=input("Rate the weld if 1 it passed if 2 gas error if 3 position: ")
        try:
            test_result = int(input_var)

            print(test_result)
            no_answer=False
        except ValueError:
            print('The provided value is not an float try again')

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

#saves all the meta data needed
def save_meta(test_nb,start_t,end_t,sample_rate_weld,sample_rate_sound,
test_result,path_sound,path_weld,path_video,t_horizontal,t_vertical,
current,voltage,wirefeed,gas_flow,discribtion,notes):

    today= datetime.today()
    test_name=today.strftime('%Y%m%d')
    list_of_inf=[[test_nb,test_name,start_t,end_t,sample_rate_weld,sample_rate_sound,test_result,
    path_sound,path_weld,path_video,t_horizontal,t_vertical,
    current,voltage,wirefeed,gas_flow,discribtion,notes]]

    df_of_inf=pd.DataFrame(list_of_inf,columns=['Test_number','Date_y_m_d','Start_time_[unix_ms]',
    'End_time_[unix_ms]','Sample_rate_weld[Hz]','Sample_rate_sound[Hz]',
    'Rating','Path_sound','Path_weld','Path_video','Thickness_hor[mm]',
    'Thickness_ver[mm]','Current[A*10]','Voltage[V*10]','Wire_feed[m/min]',
    'Gas_flow[L/min]','Describtion','Notes'])
    

    data_dir="Data/"
    data_type=["cam/","meta/","scan/","sound/","weld/"]

    cur_dir=os.listdir(data_dir+data_type[1])
    df = pd.read_csv("Data/meta/meta.csv", sep=",")

    df_param=pd.read_csv("Data/meta/00_semi_constant_param.csv",sep=',')
    df_of_inf = pd.concat([df_of_inf, df_param], ignore_index=True,axis=1, join='inner')
    df_of_inf.columns = ['Test_number','Date_y_m_d','Start_time_[unix_ms]','End_time_[unix_ms]',
    'Sample_rate_weld[Hz]','Sample_rate_sound[Hz]','Rating','Path_sound','Path_weld','Path_video',
    'Thickness_hor[mm]','Thickness_ver[mm]','Current[A*10]','Voltage[V*10]','Wire_feed[m/min]',
    'Gas_flow[L/min]','Describtion','Notes','Material','Gas_type','Electrode','Travel_speed[m/min]',
    'Electrode_d[mm]','Wire_stictout[mm]','Gun_angle','Worker_angle','Length']
    df = df.append(df_of_inf, ignore_index = True)
    print("saving data")
    
    cur_dir = os.getcwd()
    number=len(os.listdir(cur_dir+"/Data/meta"))+1
    number=f"{number:03d}"
    test_name=str(test_name)+"_"+str(test_result)+"_meta_"+str(number)+".csv"
    print(test_name)
    df.to_csv("Data/meta/meta.csv",index=False)
    return df_of_inf


#function that controls communication with the robot and starts and stops any recordings
def data_exchange_with_cowelder():
    
    

    current,voltage,wirefeed,gas_flow,t_horizontal,t_vertical,discribtion=0,0,0,0,0,0,0
    df_last_setting=0
    Hz_sound=16000
    Hz_weld=500

    current,voltage,wirefeed,gas_flow,t_horizontal,t_vertical,discribtion=meta_data(current,voltage,
                                    wirefeed,gas_flow,t_horizontal,t_vertical,discribtion,df_last_setting)
    initiate_weld_signal = input("Type 'weld' to start welding: ")

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

    
    
    try:
        while close_socket == False:
            if initiate == True:
                today= datetime.today()
                cur_dir = os.getcwd()
                number=len(os.listdir(cur_dir+"/Data/cam"))+1
                test_name=str(today.year)+str(today.month)+str(today.day)
                test_name=str(test_name)+"_cam_"+str(number)+'.mp4'
                path_video='Data/cam/'+test_name
                initiate = False
                video_getter = VideoGet(1)
            current,voltage,wirefeed,gas_flow,t_horizontal,t_vertical,discribtion=meta_data(current,voltage,
                                    wirefeed,gas_flow,t_horizontal,t_vertical,discribtion,df_last_setting)

            initiate_go_signal = input("Type 'start' to initiate program: ")
            welding_data_list = ["Current, Voltage, Wire-feed, Gas-flow"]
            if initiate_go_signal == "start": #start signal moves the robot down to airpointstart
                while initiate_weld_signal == "NULL":
                    connection.send((bytes('(1)', 'ascii'))) #Sends signal
                    recieved_data = connection.recv(1024) # waits for confirmation
                    if recieved_data == int.to_bytes(3,4,'big'):
                        welding_tip_in_position = True
                        initiate_weld_signal = input("Type 'weld' to start welding: ")
            #Starts the arc on the robot and the welding process
            if initiate_weld_signal == "weld" and welding_tip_in_position == True: 
                initiate_go_signal = "NULL"
                Micdata=Microphones.CallMic(60,16000)
                video_getter.start()
                connection.send((bytes('(2)', 'ascii')))
                unix_time_start=datetime.now()
                unix_time_start=(time.mktime(unix_time_start.timetuple())*1e3 
                + unix_time_start.microsecond/1e3)

                while weldment_done == False: 
                    connection.send((bytes('(2)', 'ascii')))
                    recieved_data = connection.recv(1024)

                    if recieved_data == int.to_bytes(4,4,'big'):
                        connection.send((bytes('(0)', 'ascii')))
                        unix_time_end=datetime.now()
                        unix_time_end=(time.mktime(unix_time_end.timetuple())*1e3 
                        + unix_time_end.microsecond/1e3)
                        Micdata=Microphones.stoprec(Micdata)
                        video_getter.stop()
                        weldment_done = True  

                    else:
                        welding_data_list.append(recieved_data.decode("utf-8"))
                welding_tip_in_position = False        
                initiate_weld_signal = "NULL"

            if weldment_done == True: #saves data
                welding_data_dataframe = pd.DataFrame(welding_data_list)
                welding_data_dataframe = welding_data_dataframe[0].str.split(',',expand=True)
                new_header = welding_data_dataframe.iloc[0] #grab the first row for the headery
                welding_data_dataframe = welding_data_dataframe[1:] #take the data less the header row
                #set the header row as the welding_data_dataframe header
                welding_data_dataframe.columns = new_header 
                lst=np.linspace(unix_time_start,unix_time_end,len(welding_data_dataframe.index))
                welding_data_dataframe['time [s]']=lst

                cols =  welding_data_dataframe.columns.tolist()
                cols = cols[-1:] + cols[:-1]
                welding_data_dataframe = welding_data_dataframe[cols]
                mic_df=pd.DataFrame(Micdata,columns=['Channel_1','Channel_2','Channel_3','Channel_4'])
                lst=np.linspace(unix_time_start,unix_time_end,len(mic_df.index))
                mic_df['time [s]']=lst
                cols =  mic_df.columns.tolist()
                cols = cols[-1:] + cols[:-1]
                mic_df = mic_df[cols]
                
                test_result,notes=comment_data()
                path_weld=save_data("weld", data=welding_data_dataframe, rating=test_result)
                path_sound=save_data("sound", data=mic_df, rating=test_result)
                df_last_settings=save_meta(number,unix_time_start,unix_time_end,Hz_weld,Hz_sound,test_result,
                path_sound,path_weld,path_video,t_horizontal,t_vertical,
                current,voltage,wirefeed,gas_flow,discribtion,notes)

                weldment_done = False

            if input("Continue to weld another piece press 'y' | shutdown press 'n': ") == "n":
                close_socket = True
                connection.send((bytes('(5)', 'ascii')))
                connection.close()
                
            else:
                initiate = True
    except: # is used if the robot stop during the welding process so data is not lost
        unix_time_end=datetime.now()
        unix_time_end=time.mktime(unix_time_end.timetuple())*1e3 + unix_time_end.microsecond/1e3
        Micdata=Microphones.stoprec(Micdata)
        video_getter.stop()
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
        mic_df=pd.DataFrame(Micdata,columns=['Channel_1','Channel_2','Channel_3','Channel_4'])
        lst=np.linspace(unix_time_start,unix_time_end,len(mic_df.index))

        mic_df['time [s]']=lst
        cols =  mic_df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        mic_df = mic_df[cols]
                
        test_result,notes=comment_data()
        path_weld=save_data("weld", data=welding_data_dataframe, rating=test_result)
        path_sound=save_data("sound", data=mic_df, rating=test_result)
        df_last_settings=save_meta(number,unix_time_start,unix_time_end,Hz_weld,Hz_sound,test_result,
        path_sound,path_weld,path_video,t_horizontal,t_vertical,
        current,voltage,wirefeed,gas_flow,discribtion,notes)
        connection.close()
        

def main():
    data_exchange_with_cowelder()


if __name__ == '__main__':
    main()