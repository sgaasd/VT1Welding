from datetime import datetime
import time
import numpy as np
import csv
import openfiles
#unix_time_start=datetime.now()
#unix_time_start=time.mktime(unix_time_start.timetuple())*1e3 + unix_time_start.microsecond/1e3

#time.sleep(10)   

#unix_time_end=datetime.now()
#unix_time_end=time.mktime(unix_time_end.timetuple())*1e3 + unix_time_end.microsecond/1e3


#print(unix_time_start)
#print(unix_time_end)

#print((unix_time_end-unix_time_start)/1e3)

lines = []
with open("Data/sound/2022128_1_sound_001.csv", 'r') as file:
    data = csv.reader(file)
    for entry in data:
        lines.append(entry)


unix_start = 1670517447 * 1000
weld_time_seconds = 28400
unix_end = unix_start + weld_time_seconds

print(unix_start)
print(unix_end)
print(unix_end-unix_start)

df_meta=openfiles.updata_df(1)
df=openfiles.df_from_path(openfiles.col_to_list(df_meta,'Path_sound'),0-1)
print(df)

lst=np.linspace(unix_start,unix_end,len(df.index))


df['time [s]']=lst

df.to_csv("Data/sound/2022128_1_sound_001.csv",index=False)

