from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtUiTools import *
from PySide6.QtWidgets import *
import cv2 
import qimage2ndarray
import sys 
import ui.dependencies as dependencies

# Displays single frame
def displayFrame():
    frame = dependencies.get_frame()
    try:
        if frame == False:
            sys.exit()
    except:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = qimage2ndarray.array2qimage(frame)
        label.setPixmap(QPixmap.fromImage(image))

app = QApplication([])
window = QWidget()

#Timer determines frame call#
timer = QTimer()
timer.timeout.connect(displayFrame)
timer.start(5)

#Quit button#
button = QPushButton("Zakończ")
button.clicked.connect(sys.exit) 

#Layout setup#
label = QLabel('No Camera Feed')
layout = QVBoxLayout()
layout.addWidget(button)
layout.addWidget(label)
window.setLayout(layout)

#Display window#
window.show()
app.exec_()