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
    button_clear_path = window.button_clear_path
    label_positions = window.label_positions
    label_path = window.label_path
    combo_items = window.combo_items
    ################    
    
    ##Variables##
    current_path = list()
    
    def __init__(self):
        ##Adding actions to buttons##
        self.button_exit.clicked.connect(sys.exit) 
        self.button_camera.clicked.connect(postition_calculating.loop) 
        self.button_add_to_path.clicked.connect(self.add_to_path)
        self.button_clear_path.clicked.connect(self.clear_path)
        ######################
        
        ##Adding items to postions list##
        self.add_items_to_label()
        
        ##Append list to comboBox##
        self.add_items_to_combo()
        
        ##Show window##
        self.show_window()

    def show_window(self):
        self.window.show()
    
    #After clicking button, func adds selected position to route#
    def add_to_path(self):
        curr_position = self.combo_items.currentText()
        self.current_path.append(curr_position)
        self.update_path_label()
    
    #Clears whole saved route#
    def clear_path(self):
        self.current_path = list()
        self.update_path_label()
    
    #Get list of num of positions eg. ['1', '2', ...] for comboBox#
    def get_list_of_pos_numbers(self):
        data_to_return = list()
        for index in range(len(postition_calculating.get_positions()) // 5):
            data_to_return.append(str(index + 1))
        return data_to_return
    
    #Append to comboBox#
    def add_items_to_combo(self):
        self.combo_items.addItems(self.get_list_of_pos_numbers())
    
    #Updates label with current route#
    def update_path_label(self):
        positions = postition_calculating.get_positions()
        self.current_path_positions = list()
        oneline_text = ""
        text_to_post = ""
        
        for index, value in enumerate(self.current_path):
            value = int(value)
            curr_pos = positions[(value - 1) * 5:(value - 1) * 5 + 5]
            self.current_path_positions.append(curr_pos)
            for i, val in enumerate(curr_pos):
                if i == 0:
                    oneline_text += f'{index + 1}. '
                elif i == 1:
                    pass
                elif i == 2:
                    oneline_text += f'X:{val} '
                elif i == 3:
                    oneline_text += f'Y:{val} '
                elif i == 4:
                    oneline_text += f'Z:{val}\n'
                    text_to_post = oneline_text
        self.label_path.setText(text_to_post)

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
    