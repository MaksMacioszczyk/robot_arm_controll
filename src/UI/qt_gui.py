from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtUiTools import *
from PySide6.QtWidgets import *
import cv2 # OpenCV
import qimage2ndarray # for a memory leak,see gist
import sys # for exiting

# Minimal implementation...

def displayFrame():
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = qimage2ndarray.array2qimage(frame)
    label.setPixmap(QPixmap.fromImage(image))

app = QApplication([])
window = QWidget()

# OPENCV

cap = cv2.VideoCapture()
cap.open("http://192.168.0.19:8000/")

# timer for getting frames

timer = QTimer()
timer.timeout.connect(displayFrame)
timer.start(60)
label = QLabel('No Camera Feed')
button = QPushButton("Quiter")
button.clicked.connect(sys.exit) # quiter button 
layout = QVBoxLayout()
layout.addWidget(button)
layout.addWidget(label)
window.setLayout(layout)
window.show()
app.exec_()