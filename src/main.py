from cvzone.HandTrackingModule import HandDetector
import cvzone
import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)
cap.open("http://192.168.0.19:8000/")
detector = HandDetector(detectionCon=0.8, maxHands=1)

isGesture = False
mariginError = 50


x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C


while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands = detector.findHands(img, draw=False)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right
        fingers1 = detector.fingersUp(hand1)
          
        if lmList1[8][0] - lmList1[4][0] <= mariginError and lmList1[8][1] - lmList1[4][1] <= mariginError and lmList1[8][2] - lmList1[4][2] <= mariginError:
            isGesture = True
        else:
            isGesture = False
            
        lmList = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
        x1, y1, _ = lmList[5]
        x2, y2, _ = lmList[17]
 
        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        A, B, C = coff
        distanceCM = A * distance ** 2 + B * distance + C
        
        fingers = detector.fingersUp(hands[0])
        if fingers == [1, 1, 1, 1, 1]:
            cvzone.putTextRect(img, f'{int(distanceCM)} cm X:{int(centerPoint1[0])} Y:{int(centerPoint1[1])}', (x+5, y-10), border=2)
        elif fingers == [1,1,0,1,1]:
            cvzone.putTextRect(img, f'{int(distanceCM)} cm X:{int(centerPoint1[0])} Y:{int(centerPoint1[1])}', (x+5, y-10))
                
        # if not isGesture:
        #     cvzone.putTextRect(img, f'{int(distanceCM)} cm X:{int(centerPoint1[0])} Y:{int(centerPoint1[1])}', (x+5, y-10), border=2)
        # else:
        #     cvzone.putTextRect(img, f'{int(distanceCM)} cm X:{int(centerPoint1[0])} Y:{int(centerPoint1[1])}', (x+5, y-10))
        
    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()