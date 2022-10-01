from cvzone.HandTrackingModule import HandDetector
import cvzone
import cv2
import numpy as np
import math
import serial


##Serial Port Init##
ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyACM0'   #DON'T  CHANGE
ser.timeout = 1
try:
    ser.open()
except:
    ser.port = 'COM3'   #CHANGE HERE
    ser.open()
ser.write(b'off')

##Camera init##
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    camera.open("http://192.168.0.20:8080")
if not camera.isOpened():
    camera.open("http://192.168.0.25:8080")
if not camera.isOpened():
    raise "Please connect camera"

##Get camera variables##
camera_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
camera_height =  camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
camera_suspension_height = 50

##Variables##
robot_max_range_CM = [10,10,10] # [X, Y, Z]
robot_arm_lengths = [20,15,10] # [A1, A2, A3]
isOn = False
isGesture = False

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
    
#One frame#
def get_frame():
    global isGesture, isOn
    success, img = camera.read()
    hands = detector.findHands(img, draw=False)  

    if hands:
        ##Reading from mediapipe output##
        hand1 = hands[0]
        lmList = hand1["lmList"] 
        bbox1 = hand1["bbox"]   
        lmList = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
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
            isGesture = False
        elif fingers == [1,1,0,1,1]:
            cvzone.putTextRect(img, f'{int(distanceCM)} cm X:{int(lmList[8][0])} Y:{int(camera_height - lmList[8][1])}', (x+5, y-10), border=3)
            if not isGesture:
                isGesture = True
                if isOn:
                    send_to_Arduino = b"off"
                    isOn = False
                else:
                    send_to_Arduino = b"on"
                    isOn = True
                ser.write(send_to_Arduino)
        elif fingers == [0,1,0,0,0]:
            #cvzone.putTextRect(img, f'{int(distanceCM)} cm X:{int(lmList[8][0])} Y:{int(camera_height - lmList[8][1])}', (x+5, y), border=3)
            cv2.circle(img, (lmList[8][0],lmList[8][1]), 10, (0,0,255),10)
            calculate_kinematics(lmList, distanceCM)
        elif fingers == [0,0,1,0,0]:
            return False
        ##########################     
    return img


##Calculating inverse kinematics##
def calculate_kinematics(lmList,distanceCM):
        ##Counting robot X Y Z based on camera output##
        robot_X = lmList[8][0]/camera_width * robot_max_range_CM[0]
        robot_Y = (1 - lmList[8][1]/camera_height) * robot_max_range_CM[1]
        robot_Z = (1 - distanceCM/camera_suspension_height) * robot_max_range_CM[2]
        #################

        ##Inverse kinematics##
        M = (robot_X**2 + robot_Y**2 - robot_arm_lengths[0]**2 - robot_arm_lengths[1]**2)/(2*robot_arm_lengths[0]*robot_arm_lengths[1])
        fi2 = np.arctan((-np.sqrt(1-M**2))/(M))
        fi1 = np.arctan(robot_Y/robot_X)-np.arctan((robot_max_range_CM[1]*np.sin(fi2))/(robot_max_range_CM[0]+robot_max_range_CM[1] * np.cos(fi2)))
        
        ##OUTPUT of inverse kinematics##
        fi1_deg = np.rad2deg(fi1)
        fi2_deg = np.rad2deg(fi2)
        ###################
        
        #print(f'FI1:{fi1_deg} FI2:{fi2_deg} Z:{robot_Z}\n') # Print angles #          
        return (fi1_deg,fi2_deg,robot_Z)
     
        
