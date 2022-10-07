from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtUiTools import *
from PySide6.QtWidgets import *
import sys, os
import utils.postition_calculating as postition_calculating

#Main window class#
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
    button_add_to_path = window.button_add_to_path
    label_positions = window.label_positions
    label_path = window.label_path
    combo_items = window.combo_items
    ################    
    
    ##Variables##

    
    def __init__(self):
        ##Adding actions to buttons##
        self.button_exit.clicked.connect(sys.exit) 
        self.button_camera.clicked.connect(postition_calculating.loop) 
        self.button_add_to_path.cliced.connect(self.add_to_path)
        ######################
        
        ##Adding items to postions list##
        self.add_items_to_label()
        
        ##Append list to comboBox##
        self.add_items_to_combo()
        
        ##Show window##
        self.show_window()

    def show_window(self):
        self.window.show()
    
    def add_to_path(self):
        
        pass
    
    #Get list of num of positions eg. ['1', '2', ...] for comboBox#
    def get_list_of_pos_numbers(self):
        data_to_return = list()
        for index in range(len(postition_calculating.get_positions()) // 5):
            data_to_return.append(str(index + 1))
        return data_to_return
    
    #Append to comboBox#
    def add_items_to_combo(self):
        self.combo_items.addItems(self.get_list_of_pos_numbers())
    
    #Add postions from positions.txt to list_positions#   
    def add_items_to_label(self):
        positions = postition_calculating.get_positions()
        text_to_post = ""
        oneline_text = ""
        count = 0
        for index, value in enumerate(positions):
            if count == 0:
                oneline_text = f'{index // 5 + 1}.'
            elif count == 1:
                pass
            elif count == 2:
                oneline_text += f' X:{value}'
            elif count == 3:
                oneline_text += f' Y:{value}'
            elif count == 4:
                oneline_text += f' Z:{value}\n'
                text_to_post += oneline_text
                oneline_text = ""
                count = 0
                continue
            count += 1
        self.label_positions.setText(text_to_post)
        
if __name__ == "__main__":
    window_application = WindowApp()
    sys.exit(window_application.app.exec())
    