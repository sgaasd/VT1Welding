
import robolink
import robodk
import time
import os
import xml.etree.ElementTree as XML
import ast
from win32com.shell import shell, shellcon
import configparser
config = configparser.ConfigParser()

config.read("C:\\Users\\simat\\OneDrive\\Desktop\\ElementaryOperations\\Horn\\example.ini")

stop_index = ast.literal_eval(config['DEFAULT']['stop'])
name_index = ast.literal_eval(config['DEFAULT']['name'])
stop_index2 = ast.literal_eval(config['DEFAULT']['stop2'])
freq = ast.literal_eval(config['DEFAULT']['freq'])
index = ast.literal_eval(config['DEFAULT']['index'])
new_speed = ast.literal_eval(config['DEFAULT']['speed'])
RDK = robolink.Robolink()

robot = RDK.Item("UR5")
RDK.setRunMode(robolink.RUNMODE_SIMULATE)

XMLFile = XML.parse(os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0), "EWO.xml"))
XMLRoot = XMLFile.getroot()
ProductMeta = XMLRoot.attrib
weldments = []
for child in XMLRoot:
    weldments.append(child)


for wldmnt in weldments:
    weld_name = ast.literal_eval(wldmnt.attrib['No'])
    robot.setSpeed(30, 10)
    approach_name = "Weldment" + str(weld_name) + "Approach"
    target = RDK.Item(approach_name)
    robot.MoveJ(target)
    robot.WaitFinished()

    ewo_name = "Weldment" + str(weld_name) + "Target0"
    target = RDK.Item(ewo_name)
    robot.MoveL(target)
    robot.WaitFinished()
    robot.setSpeed(new_speed, 10)
    input('press any key to start weldment')
    print('weldment_started')
    for ewo in wldmnt:
        
        ewo_name = "Weldment" + str(weld_name) + "Target" + str(ast.literal_eval(ewo.attrib['No']))
        target = RDK.Item(ewo_name)
        robot.MoveL(target)
        robot.WaitFinished()
    print('weldment finished')

    weld_name = ast.literal_eval(wldmnt.attrib['No'])
    robot.setSpeed(30)
    approach_name = "Weldment" + str(weld_name) + "Approach"
    target = RDK.Item(approach_name)
    robot.MoveL(target)
    robot.WaitFinished()

    


# name = None
# if freq == 0:
#     name = "TestTarget"
#     robot.setSpeed(30, 10)
#     target = RDK.Item(name + str(0))
#     target.setPose(target.Pose()*robodk.transl(0, 0, -100))
#     robot.MoveL(target)
#     robot.WaitFinished()
#     target.setPose(target.Pose()*robodk.transl(0, 0, 100))
#     target = RDK.Item(name + str(0))
#     robot.MoveL(target)
#     robot.WaitFinished()
#     #robot.setDO("0", 1)
#     weld = False
#     modified_pose = False
#     for i in range(0, index+1):
#         print('hey')
#         if not weld and i not in stop_index2:
#             print('Welding now')
#             robot.setSpeed(6.6667, 13.629392)
#             weld = True
        

#         print(i)
#         target = RDK.Item(name + str(i))
#         robot.MoveL(target)
#         robot.WaitFinished()

#         if i in stop_index2:
#             robot.setSpeed(100, 100)
#             print("Stopped welding")
#             target = RDK.Item(name + str(i))
#             target.setPose(target.Pose()*robodk.transl(0, 0, -100))
            
#             robot.MoveL(target)
#             robot.WaitFinished()
#             weld = False
#             modified_pose = True
        
#         if modified_pose:
#             target.setPose(target.Pose()*robodk.transl(0, 0, 100))
#             modified_pose=False
#         if not weld:
#             input()

# else:
#     name = "WeaveTarget"
#     robot.setSpeed(10, 10)
#     target = RDK.Item(name + str(1))
#     target.setPose(target.Pose()*robodk.transl(0, 0, -100))
#     robot.MoveL(target)
#     robot.WaitFinished()
#     target.setPose(target.Pose()*robodk.transl(0, 0, 100))
#     target = RDK.Item(name + str(2))
#     robot.MoveL(target)
#     robot.WaitFinished()
#     #robot.setDO("0", 1)
#     weld = False
#     modified_pose = False
#     for i in range(2, name_index):
#         if not weld and i not in stop_index:
#             print('Welding now')
#             robot.setSpeed(6.6667, 13.629392)
#             weld = True
#         if i in stop_index:
#             target = RDK.Item(name + str(i))
#             target.setPose(target.Pose()*robodk.transl(0, 0, -100))
#             print("Stopped welding")
#             robot.setSpeed(100, 100)
#             weld = False
#             modified_pose = True

#         print(i)
#         target = RDK.Item(name + str(i))
#         robot.MoveL(target)
#         robot.WaitFinished()
#         if modified_pose:
#             target.setPose(target.Pose()*robodk.transl(0, 0, 100))
#             modified_pose=False
#         if not weld:
#             input()
        


# # robot = RDK.Item("UR5")
# # RDK.setRunMode(robolink.RUNMODE_RUN_ROBOT)

# # for i in range(40):
# #     target = RDK.Item("WeaveTarget" + str(i+1))
# #     robot.MoveL(target)
# #     robot.WaitFinished()
