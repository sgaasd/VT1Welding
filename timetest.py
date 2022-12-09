from datetime import datetime
import time

unix_time_start=datetime.now()
unix_time_start=time.mktime(unix_time_start.timetuple())*1e3 + unix_time_start.microsecond/1e3

time.sleep(10)   

unix_time_end=datetime.now()
unix_time_end=time.mktime(unix_time_end.timetuple())*1e3 + unix_time_end.microsecond/1e3


print(unix_time_start)
print(unix_time_end)

print((unix_time_end-unix_time_start)/1e3)