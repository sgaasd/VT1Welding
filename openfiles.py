import pandas as pd
import os

import numpy as np
import open3d

def list_range(start, end, step):
    lst=[start]
    for i in range(1,end):
        start=start+step
        lst.append(start)
    return lst


#def new_measure_check(previous):
#    data_dir="Data/"
#    data_type=["cam/","info/","scan/","sound/","weld/"]
#
#    weld_dir=os.listdir(data_dir+data_type[4])
#
#    now=len(weld_dir)
#    if now != previous:
#        return True, now
#    else:
#        return False, now


def updata_df(i):
    Hz=10
    data_dir="Data/"
    data_type=["cam/","meta/","scan/","sound/","weld/"]

    cur_dir=os.listdir(data_dir+data_type[i])

    df = pd.read_csv(data_dir+data_type[i]+cur_dir[len(cur_dir)-1], sep=",")
    #print(df)
    return df




def open_scan():
    data_dir="Data/"
    data_type=["cam/","info/","scan/","sound/","weld/"]
    cur_dir=os.listdir(data_dir+data_type[2])
    pc_cur = open3d.io.read_point_cloud(data_dir+data_type[2]+cur_dir[len(cur_dir)-1])
    xyz_pc= np.asarray(pc_cur.points)
    print(xyz_pc)

    df=pd.DataFrame(data=xyz_pc, columns=['x','y','z'])
    print(df)
    return df

def path_of_vid():
    data_dir="Data/"
    data_type=["cam/","info/","scan/","sound/","weld/"]
    cur_dir=os.listdir(data_dir+data_type[0])
    path="/"+data_dir+data_type[2]+cur_dir[len(cur_dir)-1]
    return path

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
        min=df['time [s]'].min()
        max=df['time [s]'].max()
        minlist.append(min)
        maxlist.append(max)
        for i in range(0,len(minlist)-1):
            time=maxlist[i]-minlist[i]
            timelist.append(time)
    endtime=maxlist[-1]
    startime=minlist[0]
    totaltime=endtime-startime
    util=(sum(timelist)/totaltime)*100
    
    print(timelist)
    print(minlist)
    print(str(round(util,2))+'%')
    return (str(round(util,2)) + '%')

def col_to_list(df,name):
    return df[name].tolist()


def df_from_path(path_list,value):
    df = pd.read_csv(path_list[value], sep=",")
    return df

def new_measure_check(previous,list_to_check):


    now=len(list_to_check)
    if now != previous:
        return True, now
    else:
        return False, now



if __name__ == '__main__':
    df=updata_df(4)
    print(df)
    df_sound=updata_df(3)
    print(df_sound)
    #open_scan()
    vid=path_of_vid()
    print(vid)
    uptime()
    df_meta=updata_df(1)

    list_of_test=col_to_list(df_meta,'Test_number')
    df_weld=df_from_path(col_to_list(df_meta,'Path_weld'),-1)
    print(list_of_test)
    print(df_weld)
    print(new_measure_check(0,col_to_list(df_meta,'Path_weld')))
