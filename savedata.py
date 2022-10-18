import os
from datetime import datetime
import numpy as np

#List_of_csv
#array
def savedata(testtype,data,rating):
    print("saving data")
    today= datetime.today()
    testname=str(today.year)+str(today.month)+str(today.day)

    number=len(os.listdir('Data\weld'))
    testname=str(testname)+"_"+str(rating)+"_"+str(testtype)+"_"+str(number)+".csv"
    print(testname)
    np.savetxt("Data/"+str(testtype)+testname,data,delimiter=",")

weld="weld"
datatest=np.zeros(5)
savedata(weld,datatest,1)
