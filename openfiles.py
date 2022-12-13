import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import open3d
import datetime
import time

#used for updating a dataframe 
def updata_df(i):
    Hz=10
    data_dir="Data/"
    data_type=["cam/","meta/","scan/","sound/","weld/"]

    cur_dir=os.listdir(data_dir+data_type[i])

    df = pd.read_csv(data_dir+data_type[i]+cur_dir[len(cur_dir)-1], sep=",")
    if i == 4 or i==3:
        df['time [s]']=df['time [s]']-df['time [s]'].iloc[0]

    #print(df)
    return df


#returns path for the newest video
def path_of_vid():
    data_dir="Data/"
    data_type=["cam/","info/","scan/","sound/","weld/"]
    cur_dir=os.listdir(data_dir+data_type[0])
    path="/"+data_dir+data_type[2]+cur_dir[len(cur_dir)-1]
    return path

#function used for calculating the utilization rate based on unix time
def uptime():
    data_dir="Data/"
    data_type=["cam/","info/","scan/","sound/","weld/"]
    cur_dir=os.listdir(data_dir+data_type[4])
    minlist=[]
    maxlist=[]
    timelist=[]
    for i in cur_dir:
        path=data_dir+data_type[4]+i
        df = pd.read_csv(path, sep=',')
        min=df.iat[0,0]
        max=df.iat[-1,0]
        minlist.append(min)
        maxlist.append(max)
    
    for i in range(0,len(minlist)):
        time=maxlist[i]-minlist[i]
        
        timelist.append(time)
    endtime=maxlist[-1]
    startime=minlist[0]
    totaltime=endtime-startime
    util=(sum(timelist)/totaltime)*100
    
    print("minlist")
    print(minlist)

    print("maxlist")
    print(maxlist)
    print("timelist")
    print(timelist)

    print("total time testing [s]")
    print(totaltime/1000)
    print("Total time welding [s]")
    print(sum(timelist)/1000)
    print('Resulting util rate:')
    print(str(round(util,2))+'%')
    return (str(round(util,2)) + '%')

#converts a dataframe column to a list 
def col_to_list(df,name):
    return df[name].tolist()

#Opens csv as dataframe based on the path
def df_from_path(path_list,value):
    df = pd.read_csv(path_list[value], sep=",")
    df['time [s]']=df['time [s]']-df['time [s]'].iloc[0]

    return df

#check for new data
def new_measure_check(previous,list_to_check):


    now=len(list_to_check)
    if now != previous:
        return True, now
    else:
        return False, now

def numerical_int(int_var,y,m,d):
    date = datetime.date(y,m,d)

    unixtime = time.mktime(date.timetuple())

    data_dir="Data/"
    data_type=["cam/","info/","scan/","sound/","weld/"]
    cur_dir=os.listdir(data_dir+data_type[4])
    
    area=0
    arealist=[]
    timelist=[]
    for i in cur_dir:
        path=data_dir+data_type[4]+i
        df = pd.read_csv(path, sep=',')
        df_var=df[int_var].div(100)
        df_time=df['time [s]'].div(1000)
        df_time=df_time-unixtime
        df_time=df_time.div(60)


        #start values

        timelist.append(df_time.iat[0])
        arealist.append(area)

        for i in range(1,len(df_time)):
            h=df_time.iat[i]-df_time.iat[i-1]
            a=df_var.iat[i-1]
            b=df_var.iat[i]
            area=h*(1/2*(a+b))
            area=area+arealist[-1]
            arealist.append(area)
            timelist.append(df_time.iat[i])

    timelist=[x / 60 for x in timelist]

    plt.plot(timelist, arealist)
    plt.show()

def uptime_graph(y,m,d):



    data_dir="Data/"
    data_type=["cam/","info/","scan/","sound/","weld/"]
    cur_dir=os.listdir(data_dir+data_type[4])
    util_list=[]
    util_time=[]
    cur_time=0
    timelist=[]


    for i in cur_dir:
        path=data_dir+data_type[4]+i
        df = pd.read_csv(path, sep=',')
        date = datetime.date(y,m,d)
        unixtime = time.mktime(date.timetuple())
        df_time=df['time [s]'].div(1000)
        df_time=df_time-unixtime
        df_time=df_time.div(60)
        df_time=df_time.div(60)
        timelist.append(df_time.iat[0])
        util_time.append(cur_time)
        util_list.append(cur_time/(timelist[-1])*100)
        for i in range(1,len(df_time)):
            cur_time=df_time.iat[i]-df_time.iat[i-1]
            cur_time=cur_time+util_time[-1]
            util_time.append(cur_time)
            timelist.append(df_time.iat[i])

            util_list.append(cur_time/(timelist[-1])*100)

    plt.plot(timelist, util_list)
    plt.show()



        


if __name__ == '__main__':
    #df=updata_df(4)
    #print(df)
    #df_sound=updata_df(3)
    #print(df_sound)
    #open_scan()
    #vid=path_of_vid()
    #print(vid)
    uptime()
    #df_meta=updata_df(1)
    uptime_graph(2022,12,8)
    numerical_int(" Wire-feed",2022,12,8)
    numerical_int(" Gas-flow",2022,12,8)
    

    #list_of_test=col_to_list(df_meta,'Test_number')
    #df_weld=df_from_path(col_to_list(df_meta,'Path_weld'),-1)
    #print(list_of_test)
    #print(df_weld)
    #print(new_measure_check(0,col_to_list(df_meta,'Path_weld')))
