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




def new_measure_check(previous):
    data_dir="Data/"
    data_type=["cam/","info/","scan/","sound/","weld/"]

    weld_dir=os.listdir(data_dir+data_type[4])

    now=len(weld_dir)
    if now>previous:
        return True, now
    else:
        return False, now


def updata_df(i):
    Hz=10
    data_dir="Data/"
    data_type=["cam/","info/","scan/","sound/","weld/"]

    cur_dir=os.listdir(data_dir+data_type[i])

    df = pd.read_csv(data_dir+data_type[i]+cur_dir[len(cur_dir)-1], sep=",")
    #del df["Unnamed: 4"]
    print(df)
    #lst=list_range(0,len(df.index),1/Hz)
    
    #df['time [s]']=lst

    # print(lst)
    #print(len(df.index))
    #print(len(lst))

    return df


def updata_df_sound(i):
    Hz=16000
    data_dir="Data/"
    data_type=["cam/","info/","scan/","sound/","weld/"]

    cur_dir=os.listdir(data_dir+data_type[i])
    #channels=['time [s]','Channel 1','Channel 2','Channel 3','Channel 4']
    #df = pd.read_csv(data_dir+data_type[i]+cur_dir[len(cur_dir)-1], sep=',',header=None, names=channels)
    #print(df)
    df = pd.read_csv(data_dir+data_type[i]+cur_dir[len(cur_dir)-1], sep=',')

    #df['Average']=(df['Channel 1']+df['Channel 2'])/2

    #df['Frequency']=np.fft.fft(df['Average'])
    # print(lst)
    #print(len(df.index))
    #print(len(lst))
    #lst=list_range(0,len(df.index),1/Hz)
    print(df)
    #df['time [s]']=lst
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

if __name__ == '__main__':
    df=updata_df(4)
    print(df)
    df_sound=updata_df_sound(3)
    print(df_sound)
    open_scan()
    vid=path_of_vid()
    print(vid)
