from contextlib import nullcontext
from logging import exception
from xml.sax import SAXException
import robodk
import numpy as np
import xml.etree.ElementTree as XML
import ast
import robolink
from scipy import linalg
import math
from math import cos, sin
import time
import os
from win32com.shell import shell, shellcon
from scipy.spatial import distance

Speed = 0.4 * 16.67
Freq = 0
width = 1.4
alpha = math.radians(45)
beta = math.radians(0)
stickout = 20
multipass_offset = 5.6
approachDistance = 100
torch_half_diameter = 18


def transf (alpha, beta, stickout):

    row1 = [-cos(alpha), -sin(alpha)*sin(beta), -cos(beta)*sin(alpha), stickout*sin(alpha)*cos(beta)]
    row2 = [0, cos(beta), -sin(beta), stickout*sin(beta)]
    row3 = [sin(alpha), -cos(alpha)*sin(beta), -cos(alpha)*cos(beta), stickout*cos(alpha)*cos(beta)]
    row4 = [0, 0, 0, 1]

    # row1 = [1, 0, 0, 0]
    # row2 = [0, 1, 0, 0]
    # row3 = [0, 0, 1, 0]
    # row4 = [0, 0, 0, 1]

    return robodk.Mat([row1, row2, row3, row4])

XMLFile = XML.parse(os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0), "EWO.xml"))
XMLRoot = XMLFile.getroot()
ProductMeta = XMLRoot.attrib
weldments = []
for child in XMLRoot:
    weldments.append(child)

object_address = ProductMeta['STEPFile']
print(object_address)

RDK = robolink.Robolink()
TargetFrame = RDK.Item("ItemFrame")

TargetFrame.AddFile(object_address)

index = 0
start = False
StartPose = None
name_index = 1

stop_index = []
stop_index2 = []

new_speed = Speed



for wldmnt in weldments:
    start = False
    totalWeldmentLength = 0
    totalWeldmentLength2 = 0
    initialWeldmentLength = 0
    current_point = []
    amal = ast.literal_eval(wldmnt.attrib['WeldBeadSize'])
    weld_name = ast.literal_eval(wldmnt.attrib['No'])
    ewo_list = []

    for ewo in wldmnt:
        ewo_list.append(ewo)

    mid_ewo = ewo_list[int(len(ewo_list)/2 -1)]
    ApproachPose = ast.literal_eval(mid_ewo.attrib['StartPose'])
    ApproachPose[0][3] = ApproachPose[0][3] * 1000
    ApproachPose[1][3] = ApproachPose[1][3] * 1000
    ApproachPose[2][3] = ApproachPose[2][3] * 1000
    ApproachPose = robodk.Mat(ApproachPose)

    target = RDK.AddTarget("Weldment" + str(weld_name) + "Approach")
    target.setPose(ApproachPose)
    target.setPose(target.Pose()*transf(alpha, beta, stickout)*robodk.transl(0, 0, -60))
    # robot = RDK.Item("UR10e")
    robot = RDK.Item("UR5")
    robot.setSpeed(100, 500)
    RDK.setCollisionActive(0)
    robot.MoveJ(target)
    for ewo in wldmnt:
        ewo_no = ast.literal_eval(ewo.attrib['No'])
        if not start:
            StartPose = ast.literal_eval(ewo.attrib['StartPose'])
            
            StartPose[0][3] = StartPose[0][3] * 1000
            StartPose[1][3] = StartPose[1][3] * 1000
            StartPose[2][3] = StartPose[2][3] * 1000
            PreviousPosition = np.array([StartPose[0][3],
                    StartPose[1][3],
                    StartPose[2][3]])


            StartPose = robodk.Mat(StartPose)
        
            target1 = RDK.AddTarget("Weldment" + str(weld_name) + "Target" + str(0), TargetFrame)
            target1.setPose(StartPose)
            # position0 = target1.Pose()*transf(alpha, beta, stickout)*robodk.roty(math.radians(180))
            position0 = target1.Pose()*transf(alpha, beta, stickout)
            target1.setPose(position0)

            RDK.setCollisionActive(0)
            robot.MoveL(target1)
            while(robot.Busy()):
                time.sleep(0.1)

            while RDK.setCollisionActive(1):
                print(math.atan(stickout/torch_half_diameter))
                #target1.setPose(target1.Pose()*robodk.transl(0, torch_half_diameter, 0)*robodk.rotx(math.atan(stickout/torch_half_diameter)))
                target1.setPose(StartPose)
                target1.setPose(target1.Pose()*transf(alpha, math.atan(stickout/torch_half_diameter), 22))
                RDK.setCollisionActive(0)
                robot.MoveL(target1)
                while(robot.Busy()):
                    time.sleep(0.1)

                
            
            prevpos = np.array(target1.Pose().Pos())
            
            start = True
        index += 1    
        EndPose = ast.literal_eval(ewo.attrib['EndPose'])
        EndPose[0][3] = EndPose[0][3] * 1000
        EndPose[1][3] = EndPose[1][3] * 1000
        EndPose[2][3] = EndPose[2][3] * 1000
        CurrentPosition = np.array([EndPose[0][3],
                    EndPose[1][3],
                    EndPose[2][3]])
        EndPose = robodk.Mat(EndPose)

        initialWeldmentLength = initialWeldmentLength + distance.euclidean(PreviousPosition, CurrentPosition)
        currentDistance = distance.euclidean(PreviousPosition, CurrentPosition)
        
        currentT = currentDistance/Speed
        weaves = round(currentT *Freq)
        
        print(weaves)
        #dif = triangleBase
        i = 1
        # for index3 in range(weaves):
            
        #     weave_target = RDK.AddFrame("WeaveTarget" + str(i), TargetFrame)
        #     new_dif = dif*i
        #     weave_target.setPose(target1.Pose()*robodk.transl(new_dif[0], new_dif[1], new_dif[2])*robodk.transl(-width_1/math.sqrt(2), 0, width_2/math.sqrt(2)))
        #     i += 1
        #     new_dif = dif * i
        #     weave_target = RDK.AddFrame("WeaveTarget" + str(i), TargetFrame)
        #     weave_target.setPose(target1.Pose()*robodk.transl(new_dif[0], new_dif[1], new_dif[2])*robodk.transl(width_1/math.sqrt(2), 0, -width_2/math.sqrt(2)))
        # print(dif)
        target1 = RDK.AddTarget("Weldment" + str(weld_name) + "Target" + str(ewo_no), TargetFrame)
        target1.setPose(EndPose)
        # position1 = target1.Pose()*transf(alpha, beta, stickout)*robodk.roty(math.radians(180))
        position1 = target1.Pose()*transf(alpha, beta, stickout)
        target1.setPose(position1)

        RDK.setCollisionActive(0)
        robot.MoveL(target1)
        while(robot.Busy()):
            time.sleep(0.1)

        while RDK.setCollisionActive(1):
            print(math.atan(stickout/torch_half_diameter))
            #target1.setPose(target1.Pose()*robodk.transl(0, torch_half_diameter, 0)*robodk.rotx(math.atan(stickout/torch_half_diameter)))
            target1.setPose(EndPose)
            target1.setPose(target1.Pose()*transf(alpha, -math.atan(stickout/torch_half_diameter), 22))
            RDK.setCollisionActive(0)
            robot.MoveL(target1)
            while(robot.Busy()):
                time.sleep(0.1)
            
        
        # target1.setPose(target1.Pose()*transf(alpha, beta, stickout))
        # index += 1
        curpos = np.array(target1.Pose().Pos())
     
        dif = (curpos - prevpos) / (weaves*2)
        if Freq!= 0:
            triangleBase = Speed/(2*Freq)
            l= math.sqrt((width*width) + ((triangleBase*triangleBase)/4))
        
            new_speed = l*4*Freq
            print('new speed', new_speed)
            for index3 in range(weaves):
                
                weave_target = RDK.AddTarget("WeaveTarget" + str(name_index), TargetFrame)
                new_dif = dif*i
                position11 = position0.copy()
                name_index += 1
                position11[0, 3] = position0[0, 3] + new_dif[0]  
                position11[1, 3] = position0[1, 3] + new_dif[1] -  width/math.sqrt(2)
                position11[2, 3] = position0[2, 3] + new_dif[2] - width/math.sqrt(2)
                Pos1 = np.array([position11[0, 3], position11[1, 3], position11[2, 3]])
                weave_target.setPose(position11)
                
                #weave_target.setPose(weave_target.Pose()*robodk.transl(new_dif[0], new_dif[1], new_dif[2])*robodk.transl(-width_1/math.sqrt(2), 0, width_2/math.sqrt(2)))
                i += 1
                new_dif = dif * i
                weave_target = RDK.AddTarget("WeaveTarget" + str(name_index), TargetFrame)
                position12 = position0.copy()
                name_index += 1
                position12[0, 3] = position0[0, 3] + new_dif[0] 
                position12[1, 3] = position0[1, 3] + new_dif[1]+ width / math.sqrt(2)
                position12[2, 3] = position0[2, 3] + new_dif[2]+width / math.sqrt(2)
                #totalWeldmentLength = totalWeldmentLength + width_2
                Pos2 = np.array([position12[0, 3], position12[1, 3], position12[2, 3]])
                print(distance.euclidean(Pos1, Pos2))
                totalWeldmentLength = totalWeldmentLength + (width * 2 + width * 2)
                totalWeldmentLength2 = totalWeldmentLength2 + distance.euclidean(Pos1, Pos2)
                weave_target.setPose(position12)
                #weave_target.setPose(weave_target.Pose()*robodk.transl(new_dif[0], new_dif[1], new_dif[2])*robodk.transl(width_1/math.sqrt(2), 0, -width_2/math.sqrt(2)))
                i+=1

        

        PreviousPosition = CurrentPosition.copy()
        prevpos = curpos
        StartPose = EndPose
        position0 = position1
    stop_index.append(name_index-1)
    stop_index2.append(index)
    if amal > 0.007:
        start = False
        for ewo in wldmnt:
            if not start:
                StartPose = ast.literal_eval(ewo.attrib['StartPose'])
                StartPose[0][3] = StartPose[0][3] * 1000
                StartPose[1][3] = StartPose[1][3] * 1000
                StartPose[2][3] = StartPose[2][3] * 1000
                PreviousPosition = np.array([StartPose[0][3],
                        StartPose[1][3],
                        StartPose[2][3]])


                StartPose = robodk.Mat(StartPose)
            
                target1 = RDK.AddTarget("TestTarget" + str(index), TargetFrame)
                target1.setPose(StartPose)
                # position0 = target1.Pose()*transf(alpha, beta, stickout)*robodk.roty(math.radians(180))
                position0 = target1.Pose()*transf(alpha, beta, stickout)
                target1.setPose(position0)
                prevpos = np.array(target1.Pose().Pos())
                
                start = True
            index += 1    
            EndPose = ast.literal_eval(ewo.attrib['EndPose'])
            EndPose[0][3] = EndPose[0][3] * 1000
            EndPose[1][3] = EndPose[1][3] * 1000
            EndPose[2][3] = EndPose[2][3] * 1000
            CurrentPosition = np.array([EndPose[0][3],
                        EndPose[1][3],
                        EndPose[2][3]])
            EndPose = robodk.Mat(EndPose)

            #initialWeldmentLength = initialWeldmentLength + distance.euclidean(PreviousPosition, CurrentPosition)
            currentDistance = distance.euclidean(PreviousPosition, CurrentPosition)
            
            currentT = currentDistance/Speed
            weaves = round(currentT *Freq)
            print(weaves)
            dif = (CurrentPosition - PreviousPosition) / (weaves*2)
            i = 1
            # for index3 in range(weaves):
                
            #     weave_target = RDK.AddFrame("WeaveTarget" + str(i), TargetFrame)
            #     new_dif = dif*i
            #     weave_target.setPose(target1.Pose()*robodk.transl(new_dif[0], new_dif[1], new_dif[2])*robodk.transl(-width_1/math.sqrt(2), 0, width_2/math.sqrt(2)))
            #     i += 1
            #     new_dif = dif * i
            #     weave_target = RDK.AddFrame("WeaveTarget" + str(i), TargetFrame)
            #     weave_target.setPose(target1.Pose()*robodk.transl(new_dif[0], new_dif[1], new_dif[2])*robodk.transl(width_1/math.sqrt(2), 0, -width_2/math.sqrt(2)))
            # print(dif)
            target1 = RDK.AddTarget("TestTarget" + str(index), TargetFrame)
            target1.setPose(EndPose)
            # position1 = target1.Pose()*transf(alpha, beta, stickout)*robodk.roty(math.radians(180))
            position1 = target1.Pose()*transf(alpha, beta, stickout)
            target1.setPose(position1)
            # target1.setPose(target1.Pose()*transf(alpha, beta, stickout))
            # index += 1
            curpos = np.array(target1.Pose().Pos())
        
            dif = (curpos - prevpos) / (weaves*2)
            if weaves != 0:
                for index3 in range(weaves):
                    
                    weave_target = RDK.AddTarget("WeaveTarget" + str(name_index), TargetFrame)
                    new_dif = dif*i
                    position11 = position0.copy()
                    name_index += 1
                    position11[0, 3] = position0[0, 3] + new_dif[0]  
                    position11[1, 3] = position0[1, 3] + new_dif[1]   -width/math.sqrt(2) - multipass_offset
                    position11[2, 3] = position0[2, 3] + new_dif[2]  -width/math.sqrt(2)
                    #totalWeldmentLength = totalWeldmentLength + width_1
                    weave_target.setPose(position11)
                    #weave_target.setPose(weave_target.Pose()*robodk.transl(new_dif[0], new_dif[1], new_dif[2])*robodk.transl(-width_1/math.sqrt(2), 0, width_2/math.sqrt(2)))
                    i += 1
                    new_dif = dif * i
                    weave_target = RDK.AddTarget("WeaveTarget" + str(name_index), TargetFrame)
                    position12 = position0.copy()
                    name_index += 1
                    position12[0, 3] = position0[0, 3] + new_dif[0] 
                    position12[1, 3] = position0[1, 3] + new_dif[1]+ width / math.sqrt(2) - multipass_offset
                    position12[2, 3] = position0[2, 3] + new_dif[2]+width / math.sqrt(2)
                    #totalWeldmentLength = totalWeldmentLength + width_2
                    weave_target.setPose(position12)
                    #weave_target.setPose(weave_target.Pose()*robodk.transl(new_dif[0], new_dif[1], new_dif[2])*robodk.transl(width_1/math.sqrt(2), 0, -width_2/math.sqrt(2)))
                    i+=1

                

            PreviousPosition = CurrentPosition.copy()
            prevpos = curpos
            StartPose = EndPose
            position0 = position1

        stop_index.append(name_index-1)
        start = False
        for ewo in wldmnt:
            if not start:
                StartPose = ast.literal_eval(ewo.attrib['StartPose'])
                StartPose[0][3] = StartPose[0][3] * 1000
                StartPose[1][3] = StartPose[1][3] * 1000
                StartPose[2][3] = StartPose[2][3] * 1000
                PreviousPosition = np.array([StartPose[0][3],
                        StartPose[1][3],
                        StartPose[2][3]])


                StartPose = robodk.Mat(StartPose)
            
                target1 = RDK.AddTarget("TestTarget" + str(index), TargetFrame)
                target1.setPose(StartPose)
                # position0 = target1.Pose()*transf(alpha, beta, stickout)*robodk.roty(math.radians(180))
                position0 = target1.Pose()*transf(alpha, beta, stickout)
                target1.setPose(position0)
                prevpos = np.array(target1.Pose().Pos())
                
                start = True
            index += 1    
            EndPose = ast.literal_eval(ewo.attrib['EndPose'])
            EndPose[0][3] = EndPose[0][3] * 1000
            EndPose[1][3] = EndPose[1][3] * 1000
            EndPose[2][3] = EndPose[2][3] * 1000
            CurrentPosition = np.array([EndPose[0][3],
                        EndPose[1][3],
                        EndPose[2][3]])
            EndPose = robodk.Mat(EndPose)

            #initialWeldmentLength = initialWeldmentLength + distance.euclidean(PreviousPosition, CurrentPosition)
            currentDistance = distance.euclidean(PreviousPosition, CurrentPosition)
            
            currentT = currentDistance/Speed
            weaves = round(currentT *Freq)
            print(weaves)
            dif = (CurrentPosition - PreviousPosition) / (weaves*2)
            i = 1
            # for index3 in range(weaves):
                
            #     weave_target = RDK.AddFrame("WeaveTarget" + str(i), TargetFrame)
            #     new_dif = dif*i
            #     weave_target.setPose(target1.Pose()*robodk.transl(new_dif[0], new_dif[1], new_dif[2])*robodk.transl(-width_1/math.sqrt(2), 0, width_2/math.sqrt(2)))
            #     i += 1
            #     new_dif = dif * i
            #     weave_target = RDK.AddFrame("WeaveTarget" + str(i), TargetFrame)
            #     weave_target.setPose(target1.Pose()*robodk.transl(new_dif[0], new_dif[1], new_dif[2])*robodk.transl(width_1/math.sqrt(2), 0, -width_2/math.sqrt(2)))
            # print(dif)
            target1 = RDK.AddTarget("TestTarget" + str(index), TargetFrame)
            target1.setPose(EndPose)
            # position1 = target1.Pose()*transf(alpha, beta, stickout)*robodk.roty(math.radians(180))
            position1 = target1.Pose()*transf(alpha, beta, stickout)
            target1.setPose(position1)
            # target1.setPose(target1.Pose()*transf(alpha, beta, stickout))
            # index += 1
            curpos = np.array(target1.Pose().Pos())
        
            dif = (curpos - prevpos) / (weaves*2)
            if weaves != 0:
                for index3 in range(weaves):
                    
                    weave_target = RDK.AddTarget("WeaveTarget" + str(name_index), TargetFrame)
                    new_dif = dif*i
                    position11 = position0.copy()
                    name_index += 1
                    position11[0, 3] = position0[0, 3] + new_dif[0]  
                    position11[1, 3] = position0[1, 3] + new_dif[1]   -width/math.sqrt(2)
                    position11[2, 3] = position0[2, 3] + new_dif[2]  -width/math.sqrt(2) + multipass_offset
                    #totalWeldmentLength = totalWeldmentLength + width_1
                    weave_target.setPose(position11)
                    #weave_target.setPose(weave_target.Pose()*robodk.transl(new_dif[0], new_dif[1], new_dif[2])*robodk.transl(-width_1/math.sqrt(2), 0, width_2/math.sqrt(2)))
                    i += 1
                    new_dif = dif * i
                    weave_target = RDK.AddTarget("WeaveTarget" + str(name_index), TargetFrame)
                    position12 = position0.copy()
                    name_index += 1
                    position12[0, 3] = position0[0, 3] + new_dif[0] 
                    position12[1, 3] = position0[1, 3] + new_dif[1]+ width / math.sqrt(2)
                    position12[2, 3] = position0[2, 3] + new_dif[2]+width / math.sqrt(2) + multipass_offset
                    #totalWeldmentLength = totalWeldmentLength + width_2
                    weave_target.setPose(position12)
                    #weave_target.setPose(weave_target.Pose()*robodk.transl(new_dif[0], new_dif[1], new_dif[2])*robodk.transl(width_1/math.sqrt(2), 0, -width_2/math.sqrt(2)))
                    i+=1

            

            PreviousPosition = CurrentPosition.copy()
            prevpos = curpos
            StartPose = EndPose
            position0 = position1
        stop_index.append(name_index-1)

t = initialWeldmentLength / Speed

#new_speed = totalWeldmentLength / t
print(Speed)
print(initialWeldmentLength)
print(t)
print(totalWeldmentLength)
print(new_speed)
print(totalWeldmentLength2)
print(totalWeldmentLength2 / t)
robot.setJoints([-70.78, -117.52, -63.89, -88.62, 90.32, -160.87])
import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {"stop":str(stop_index), "name":str(name_index), "freq":str(Freq), "stop2":str(stop_index2), "index":str(index), "speed":str(new_speed)}

with open('C:\\Users\\simat\\OneDrive\\Desktop\\ElementaryOperations\\Horn\\example.ini', 'w') as configfile:
   config.write(configfile)
"""
robot = RDK.Item("UR5")
RDK.setRunMode(robolink.RUNMODE_SIMULATE)




robot.setSpeed(10, 10)
target = RDK.Item("WeaveTarget" + str(1))
target.setPose(target.Pose()*robodk.transl(0, 0, -100))
robot.MoveL(target)
robot.WaitFinished()
target = RDK.Item("WeaveTarget" + str(2))
robot.MoveL(target)
robot.WaitFinished()
#robot.setDO("0", 1)
weld = False
for i in range(2, name_index):
    if not weld and i-1 not in stop_index:
        print('Welding now')
        weld = True
    if i in stop_index:
        target = RDK.Item("WeaveTarget" + str(i))
        target.setPose(target.Pose()*robodk.transl(0, 0, -100))
        print("Stopped welding")
        weld = False

    print(i)
    target = RDK.Item("WeaveTarget" + str(i))
    robot.MoveL(target)
    robot.WaitFinished()
    if not weld:
        input()
    


# robot = RDK.Item("UR5")
# RDK.setRunMode(robolink.RUNMODE_RUN_ROBOT)

# for i in range(40):
#     target = RDK.Item("WeaveTarget" + str(i+1))
#     robot.MoveL(target)
#     robot.WaitFinished()

print(totalWeldmentLength)

print(Speed)
t = totalWeldmentLength/Speed

print (t)

"""