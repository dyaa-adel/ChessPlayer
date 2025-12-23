from PyQt5.QtWidgets import QLabel, QColorDialog , QFileDialog, QMessageBox ,QLineEdit, QWidget , QPushButton , QHBoxLayout , QVBoxLayout , QComboBox
from PyQt5.QtCore import QDir
import os
import json

def show_no_settings_msgbox():
    """
    Show a no settings found message box
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText("Couldn't find a settings.json file in settings folder \n creating one.")
    msg.setWindowTitle('Chess Player - No Settings File Found')
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()

default_settings = '{"Arrow Thickness": "5", "Arrow Color": "#ff0004", "Engine Time Limit": "3", "Engine Path": ""}'

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class SettingsManager(metaclass=Singleton):
    """
    The SettingsManager class - it is a singeleton
    """
    def __init__(self):
        self.settings_path = os.path.join(os.path.expanduser("~"), ".chess_player_settings")
        if not os.path.exists(self.settings_path):
             os.makedirs(self.settings_path)
        self.settings_path += os.sep
        self.loadSettings()
    
    def loadSettings(self):
        """
        Load settings from seetings/settings.json file 
        """
        try:
            with open(self.settings_path + 'settings.json',"r") as f:
                self.settings = json.loads(f.read())
        except OSError:
            show_no_settings_msgbox()
            print("No settings file found , Creating one")
            f= open(self.settings_path + 'settings.json',"w+")
            f.write(default_settings) 
            f.close()
        
    def get_settings(self):
        """
        Return current settings to the caller
        """
        self.loadSettings() #TODO Remove as it was introduced to fix a bug
        return self.settings

    def updateSettings(self,key,value):
        """
        Update given setting name with given value
        """
        self.settings[key] = value

    def saveCurrentSettings(self):
        """
        Save current settings object to settings/settings.json
        """
        with open(self.settings_path + 'settings.json', "r+") as f:
            f.seek(0)
            f.write(json.dumps(self.settings))
            f.truncate()
        self.closeUI()


    def insertRow(self,setting_name , setting_value):
        """
        Add a string/number setting row to the UI
        """
        h_layout = QHBoxLayout()
        setting_label = QLabel(setting_name)
        setting_label.setFixedWidth(self.settingsWindow.width()//3)
        setting_label.setWordWrap(True)
        h_layout.addWidget(setting_label)
        setting_lineEdit = QLineEdit()
        setting_lineEdit.setText(setting_value)
        setting_lineEdit.setFixedWidth(self.settingsWindow.width()//2)
        #TODO add invalid values / error checking
        setting_lineEdit.textChanged.connect(lambda: self.updateSettings(setting_name,setting_lineEdit.text()))
        h_layout.addWidget(setting_lineEdit)

        return h_layout

    def insertRow_FilePath(self,setting_name , setting_value):
        """
        Add a filepath setting row to the UI
        """
        h_layout = QHBoxLayout()
        setting_label = QLabel(setting_name)
        setting_label.setFixedWidth(self.settingsWindow.width()//3)
        setting_label.setWordWrap(True)
        h_layout.addWidget(setting_label)
        setting_lineEdit = QLineEdit()
        setting_lineEdit.setText(setting_value)
        setting_lineEdit.setReadOnly(True)
        h_layout.addWidget(setting_lineEdit)
        setting_changeFileButton = QPushButton("Change")
        setting_changeFileButton.setFixedWidth(30)
        setting_changeFileButton.setObjectName("small")
        setting_changeFileButton.clicked.connect(lambda : self.showEngineDialog(setting_lineEdit,setting_name))
        h_layout.addWidget(setting_changeFileButton)

        return h_layout

    def insertRow_Color(self,setting_name , setting_value):
        """
        Add a Color setting row to the UI
        """
        h_layout = QHBoxLayout()
        setting_label = QLabel(setting_name)
        setting_label.setFixedWidth(self.settingsWindow.width()//3)
        setting_label.setWordWrap(True)
        h_layout.addWidget(setting_label)
        setting_value_label = QLabel(setting_value)
        setting_value_label.setStyleSheet('color : ' + setting_value)
        h_layout.addWidget(setting_value_label)
        setting_changeColorButton = QPushButton("Change")
        setting_changeColorButton.setFixedWidth(30)
        setting_changeColorButton.setObjectName("small")
        setting_changeColorButton.clicked.connect(lambda : self.showColorDialog(setting_value_label,setting_name))
        h_layout.addWidget(setting_changeColorButton)

        return h_layout



    def createUI(self):
        """
        Create settings window UI
        """
        self.loadSettings()

        #Configure Window
        self.settingsWindow = QWidget() 
        self.settingsWindow.setObjectName("window")

        self.settingsWindow.setWindowTitle("Chess Player - Settings")
        self.settingsWindow.setFixedWidth(500)



        #Window main layout
        v_layout = QVBoxLayout() # mainWindow layout

        #Top
        settings_top_label = QLabel("Settings") #TODO Modify
        
        #Middle
        for key in self.settings:
            if key == "Engine Path":
                layout = self.insertRow_FilePath(key,self.settings[key])
            
            elif 'Color' in key:
                layout = self.insertRow_Color(key,self.settings[key])
            else:
                layout = self.insertRow(key,self.settings[key])
            v_layout.addLayout(layout)

        #Bottom
        h_layout = QHBoxLayout() 

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.saveCurrentSettings)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.closeUI)

        h_layout.addWidget(self.save_button)
        h_layout.addWidget(self.cancel_button)
        v_layout.addLayout(h_layout)
        self.settingsWindow.setFixedSize(self.settingsWindow.sizeHint()) #Disable resize
        self.settingsWindow.setLayout(v_layout) 


    def showUI(self):
        self.settingsWindow.show()

    def closeUI(self):
        self.loadSettings()
        self.settingsWindow.close()

    def showEngineDialog(self,line_edit,setting_name):
        """
        Show Select Engine File Dialog
        """
        fname = QFileDialog.getOpenFileName(self.settingsWindow, 'Select Chess Engine', QDir.currentPath())
        if(fname[0]):
            self.updateSettings(setting_name,fname[0])
            line_edit.setText(fname[0])

    def showColorDialog(self,label,setting_name):
        """
        Show Color picker
        """
        color = QColorDialog.getColor()

        if color.isValid():
            self.updateSettings(setting_name,color.name())
            label.setText(color.name())
            label.setStyleSheet('color : ' + color.name())






