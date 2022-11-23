import os
from datetime import datetime
import numpy as np


def savedata(testtype,data,rating):
    print("saving data")
    today= datetime.today()
    testname=str(today.year)+str(today.month)+str(today.day)
    curdir = os.getcwd()
    number=len(os.listdir(curdir+"\Data\weld"))+1
    number=f"{number:03d}"
    testname=str(testname)+"_"+str(rating)+"_"+str(testtype)+"_"+str(number)+".csv"
    print(testname)
    np.savetxt("Data/"+str(testtype)+"/"+testname,data,delimiter=",")

weld="weld"
datatest=np.zeros(5)
savedata(weld,datatest,1)