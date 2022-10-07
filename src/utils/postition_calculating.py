from cvzone.HandTrackingModule import HandDetector
import cvzone
import cv2
import numpy as np
import math
import os 
import utils.communication as comm

##Camera init##
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    camera.open("http://192.168.0.20:8080")
if not camera.isOpened():
    camera.open("http://192.168.0.25:8080")
if not camera.isOpened():
    print("Please connect camera")
    
##Get camera variables##
camera_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
camera_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
camera_suspension_height = 50

##Variables##
robot_max_range_CM = [10,10,10] # [X, Y, Z]
robot_arm_lengths = [20,15,10] # [A1, A2, A3]
is_gesture_grip = False
is_gesture_position = False
positions_file = os.getcwd() + "/src/utils/positions.txt"
last_pos = (0,0,0,0,0)
counted_frame_to_send = 0
how_many_messages_send = 20
pos_round = 2

##Distance shenanigans##
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C
detector = HandDetector(detectionCon=0.8, maxHands=1)

def loop():
    while True:
        img = get_frame()
        try:
            if img == False:
                cv2.destroyAllWindows()
                return
        except:
            ##Print image##       
            cv2.imshow("Image", img)
            cv2.waitKey(1)
            ###############
        
#Save current position to file#
def save_postion(fi1,fi2,X,Y,Z):
    if X == 0 and Y == 0 and Z == 0:
        return
    pos = [str(fi1) + '\n', str(fi2) + '\n',str(X) + '\n', str(Y) + '\n', str(Z) + '\n']
    print(pos)
    with open(positions_file, "a") as file:
        file.writelines(pos)
        
#Get postitions from file#
def get_positions():
    with open(positions_file, "r") as file:
        data = list()
        for line in file:
            data.append(float(line))
    return data

#Returns given position#
def get_position(pos):
    with open(positions_file, "r") as file:
        data = list()
        for index, line in enumerate(file):
            if index > (pos - 1) * 5 - 1:
                data.append(float(line))
                if index >= (pos - 1) * 5 + 5:
                    break
    return data

#One frame#
def get_frame():
    global is_gesture_grip, is_gesture_position, last_pos, counted_frame_to_send, how_many_messages_send
    _, img = camera.read()
    hands = detector.findHands(img, draw=False)  

    if hands:
        ##Reading from mediapipe output##
        hand1 = hands[0]
        lmList = hand1["lmList"]   
        lmList = hands[0]['lmList']
        x, y, _, _ = hands[0]['bbox']
        x1, y1, _ = lmList[5]
        x2, y2, _ = lmList[17]
        #####################
        
        ##Measuring distance##
        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        A, B, C = coff
        distanceCM = A * distance ** 2 + B * distance + C
        #####################
        
        ##Gestures recognition##
        fingers = detector.fingersUp(hands[0])
        if fingers == [1, 1, 1, 1, 1]:
            cvzone.putTextRect(img, f'{int(distanceCM)} cm X:{int(lmList[8][0])} Y:{int(camera_height - lmList[8][1])}', (x+5, y-10), border=2)
            is_gesture_grip = False
            is_gesture_position = False
        elif fingers == [1,1,0,1,1]:
            cvzone.putTextRect(img, f'{int(distanceCM)} cm X:{int(lmList[8][0])} Y:{int(camera_height - lmList[8][1])}', (x+5, y-10), border=3)
            if not is_gesture_grip:
                is_gesture_grip = True
                
        elif fingers == [0,1,0,0,0]:
            #cvzone.putTextRect(img, f'{int(distanceCM)} cm X:{int(lmList[8][0])} Y:{int(camera_height - lmList[8][1])}', (x+5, y), border=3)
            cv2.circle(img, (lmList[8][0],lmList[8][1]), 10, (0,0,255),10)
            last_pos = calculate_kinematics(lmList, distanceCM)
            if counted_frame_to_send == how_many_messages_send:
                comm.send_fi_to_Arduino(last_pos[0], 2)
                comm.send_fi_to_Arduino(last_pos[1], 3)
                counted_frame_to_send = 0
            else:
                counted_frame_to_send += 1
            is_gesture_position = False
        elif fingers == [0,1,1,0,0]:
            if not is_gesture_position:
                is_gesture_position = True
                save_postion(last_pos[0],last_pos[1],round(last_pos[2],pos_round),round(last_pos[3],pos_round),round(last_pos[4],pos_round))
        elif fingers == [0,0,1,0,0]:
            return False
        ##########################     
    return img


##Calculating inverse kinematics##
def calculate_kinematics(lmList,distanceCM):
        ##Counting robot X Y Z based on camera output##
        robot_X = (lmList[8][0] - (camera_width // 2))/camera_width * robot_max_range_CM[0]
        robot_Y = (1 - lmList[8][1]/camera_height) * robot_max_range_CM[1]
        robot_Z = (1 - distanceCM/camera_suspension_height) * robot_max_range_CM[2]
        #################

        ##Inverse kinematics##
        try:
            M = (robot_X**2 + robot_Y**2 - robot_arm_lengths[0]**2 - robot_arm_lengths[1]**2)/(2*robot_arm_lengths[0]*robot_arm_lengths[1])
            fi2 = np.arctan((-np.sqrt(1-M**2))/(M))
            fi1 = np.arctan(robot_Y/robot_X)-np.arctan((robot_max_range_CM[1]*np.sin(fi2))/(robot_max_range_CM[0]+robot_max_range_CM[1] * np.cos(fi2)))
        except:
            print("Division by zero!!")    
            return
        
        ##OUTPUT of inverse kinematics##
        fi1_deg = np.rad2deg(fi1)
        fi2_deg = np.rad2deg(fi2)
        ###################
        
        print(f'FI1:{fi1_deg} FI2:{fi2_deg} Z:{robot_Z}\n') # Print angles #          
        return (fi1_deg,fi2_deg,robot_X, robot_Y, robot_Z)
     
        
