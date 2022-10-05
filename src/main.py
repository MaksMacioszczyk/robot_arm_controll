from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtUiTools import *
from PySide6.QtWidgets import *
import sys, os
import utils.postition_calculating as postition_calculating

class WindowApp:
    ##Qt Init##
    app = QApplication([])
    ui_file = QFile(os.getcwd() + '/src/utils/form.ui')
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ################
    
    ##Qt variables##
    button_exit = window.button_exit
    button_camera = window.button_camera
    ################
    
    def __init__(self):
        self.button_exit.clicked.connect(sys.exit) 
        self.button_camera.clicked.connect(postition_calculating.loop) 

        self.show_window()

    def show_window(self):
        self.window.show()
        
        
if __name__ == "__main__":
    window_application = WindowApp()
    sys.exit(window_application.app.exec())
    