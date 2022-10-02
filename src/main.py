from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtUiTools import *
from PySide6.QtWidgets import *
import sys 
import ui.dependencies as dependencies

app = QApplication([])
window = QWidget()

#Quit button#
button = QPushButton("Zakończ")
button.clicked.connect(sys.exit) 

#Camera button#
button_camera = QPushButton("Włącz kamere")
button_camera.clicked.connect(dependencies.loop) 

#Layout setup#
layout = QVBoxLayout()
layout.addWidget(button)
layout.addWidget(button_camera)
window.setLayout(layout)

#Display window#
window.show()
app.exec_()