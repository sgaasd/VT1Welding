from tracemalloc import start
import robolink
import robodk
import math
import time
import os
import xml.etree.ElementTree as XML
import ast
from win32com.shell import shell, shellcon
import configparser
config = configparser.ConfigParser()
RDK = robolink.Robolink()
robot = RDK.Item("UR5")
RDK.setRunMode(robolink.RUNMODE_SIMULATE)

speed = 6
XMLFile = XML.parse(os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0), "EWO.xml"))
XMLRoot = XMLFile.getroot()
ProductMeta = XMLRoot.attrib
weldments = []
for child in XMLRoot:
    weldments.append(child)

weldments_program = []

for wldmnt in weldments:
    ewo_program = []
    weld_name = ast.literal_eval(wldmnt.attrib['No'])
    robot.setSpeed(50, 100)
    approach_name = "Weldment" + str(weld_name) + "Approach"
    target = RDK.Item(approach_name)
    robot.MoveJ(target)
    robot.WaitFinished()
    ewo_program.append(robot.Joints().list())

    ewo_name = "Weldment" + str(weld_name) + "Target0"
    target = RDK.Item(ewo_name)
    robot.MoveL(target)
    robot.WaitFinished()
    robot.setSpeed(50)
    #input('press any key to start weldment')
    print('weldment_started')
    ewo_program.append(robot.Joints().list())
    for ewo in wldmnt:
        pos1 = target.Pose()*robodk.transl(0, 0, 22).Pos()
        print(pos1, 'here')
        ewo_name = "Weldment" + str(weld_name) + "Target" + str(ast.literal_eval(ewo.attrib['No']))
        target = RDK.Item(ewo_name)
        pos2 = target.Pose()*robodk.transl(0, 0, 22).Pos()
        distance = math.dist(pos1, pos2)
        pos_t = distance/speed
        robot.MoveL(target)
        robot.WaitFinished()
        p_list = robot.Joints().list()
        p_list.append(pos_t)
        ewo_program.append(p_list)
    print('weldment finished')

    weld_name = ast.literal_eval(wldmnt.attrib['No'])
    robot.setSpeed(50)
    approach_name = "Weldment" + str(weld_name) + "Approach"
    target = RDK.Item(approach_name)
    robot.MoveL(target)
    robot.WaitFinished()
    ewo_program.append(robot.Joints().list())
    weldments_program.append(ewo_program)



for weldment in weldments_program:
    approach = weldment[0]
    print('approach')
    print(approach)

    start_point = weldment[1]
    print('start_point')
    print(start_point)
    print('start_welding')
    for i in range(2, len(weldment)-1):
        print(weldment[i])

    print('stop_weldment')
    print('departure')
    print(weldment[len(weldment)-1])
    
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 50000))
s.listen(1)
conn, addr = s.accept()

print(conn)
print(addr)

data = conn.recv(8)
print(data)
acc = 0.1
speed = 0.2
time_m = 0
blend = 0
for weldment in weldments_program:
    approach = weldment[0]
    print('approach')
    print(approach)
    conn.send((bytes('(3, ' + str(math.radians(approach[0])) + ', ' + str(math.radians(approach[1])) + ', ' + str(math.radians(approach[2])) + ', ' + str(math.radians(approach[3])) + ', ' + str(math.radians(approach[4])) + ', ' + str(math.radians(approach[5])) + ', ' + str(acc) + ', ' + str(speed) + ', ' + str(time_m) + ', ' + str(blend) + ')', 'ascii')))

    data = conn.recv(8)
    print(data)

    start_point = weldment[1]
    print('start_point')
    print(start_point)
    conn.send((bytes('(3, ' + str(math.radians(start_point[0])) + ', ' + str(math.radians(start_point[1])) + ', ' + str(math.radians(start_point[2])) + ', ' + str(math.radians(start_point[3])) + ', ' + str(math.radians(start_point[4])) + ', ' + str(math.radians(start_point[5])) +  ', ' + str(acc) + ', ' + str(speed) + ', ' + str(time_m) + ', ' + str(blend) + ')', 'ascii')))

    data = conn.recv(8)
    print(data)
    print('start_welding')
    r = 1
    for i in range(2, len(weldment)-1):
        print(weldment[i])
        conn.send((bytes('(4, ' + str(math.radians(weldment[i][0])) + ', ' + str(math.radians(weldment[i][1])) + ', ' + str(math.radians(weldment[i][2])) + ', ' + str(math.radians(weldment[i][3])) + ', ' + str(math.radians(weldment[i][4])) + ', ' + str(math.radians(weldment[i][5])) + ', ' + str(2) + ', ' + str(0.00666667) + ', ' + str(weldment[i][6]) + ', ' + str(0.005) + ')', 'ascii')))
        data = conn.recv(8)
        print(r, data)
        r += 1
    print('stop_weldment')
    print('departure')
    print(weldment[len(weldment)-1])
    conn.send((bytes('(4, ' + str(math.radians(weldment[len(weldment)-1][0])) + ', ' + str(math.radians(weldment[len(weldment)-1][1])) + ', ' + str(math.radians(weldment[len(weldment)-1][2])) + ', ' + str(math.radians(weldment[len(weldment)-1][3])) + ', ' + str(math.radians(weldment[len(weldment)-1][4])) + ', ' + str(math.radians(weldment[len(weldment)-1][5])) + ', ' + str(acc) + ', ' + str(speed) + ', ' + str(time_m) + ', ' + str(blend) + ')', 'ascii')))
    data = conn.recv(8)
    print(data)
    
conn.send((bytes('(9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999)', 'ascii')))

data = conn.recv(8)
print(data)

conn.close()