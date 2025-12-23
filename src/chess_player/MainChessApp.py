from PyQt5.QtWidgets import QApplication , QLabel , QWidget , QPushButton , QHBoxLayout , QVBoxLayout , QComboBox , QMessageBox
from PyQt5.QtGui import QFont , QFontDatabase
from PyQt5.QtCore import QDir , Qt
from PyQt5.QtGui import QIcon
from .app_styles import app_styles
from .board_extraction import *
from .board_state_utils import *
from .ChessPlayer import *
from .SettingsManager import SettingsManager
from .show_move import board_with_move
import time
import pyautogui 
from numpy import array
import os

def get_screen_image(window):
    """
    Takes screenshot from the user screen using pyautogui module
    """
    window.hide()
    time.sleep(1)
    image = pyautogui.screenshot() 
    
    # since the pyautogui takes as a  
    # PIL(pillow) and in RGB we need to  
    # convert it to numpy array and BGR  
    # so we can write it to the disk 
    image = cv2.cvtColor(array(image),cv2.COLOR_RGB2BGR) 
    cv2.imwrite("screenshot_taken.png", image) 
    window.show()
    return image

class MainChessApp():
    """
    The main application class
    """
    def __init__(self):
        self.player = None #New Player
        self.app = QApplication([]) 
        dir_ = QDir("fonts") #Set working directory
        #Set application details and icon
        self.app.setApplicationName("Chess Player") 
        self.app.setApplicationDisplayName("Chess Player")
        base_path = os.path.dirname(__file__)
        self.app.setWindowIcon(QIcon(os.path.join(base_path, "icons/chess_icon.ico")))

        #Get SettingsManager Instance
        self.settingsManager = SettingsManager()

        
    def buildUI(self):
        """
        Build main window UI
        """
        #Add The font
        base_path = os.path.dirname(__file__)
        _id = QFontDatabase.addApplicationFont(os.path.join(base_path, "fonts/CenturyGothic.ttf"))

        #set the application style
        self.setAppStyle()

        #Configure Window
        self.mainWindow = QWidget() 
        self.mainWindow.setObjectName('window')
        self.mainWindow.setWindowTitle("Chess Player")

        #Window main layout
        v_layout = QVBoxLayout() # mainWindow layout
        h_layout = QHBoxLayout() # Placeholder for mainWindow buttons

        #Top Section
        logo = QLabel("Chess Player")
        logo_font = QFont("CenturyGothic", 38, QFont.Bold) 
        logo.setFont(logo_font)
        logo.setStyleSheet("color: #0B5394;")
        v_layout.addWidget(logo) 

        #Bottom Section
        self.capture_button = QPushButton("Start Capturing Board")
        self.capture_button.clicked.connect(self.captureBoard)

        self.motivation_button = QPushButton("Last Move")
        self.motivation_button.clicked.connect(lambda : self.showLastMove())

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.openSettings)

        h_layout.addWidget(self.capture_button)
        h_layout.addWidget(self.motivation_button)
        h_layout.addWidget(self.settings_button)

        #Finalize layout
        v_layout.addLayout(h_layout)
        self.mainWindow.setLayout(v_layout) 

        #Configure Window settings
        self.mainWindow.setFixedSize(self.mainWindow.sizeHint()) #Disable resize
        self.mainWindow.show()
        self.app.exec_()

    def setAppStyle(self):
        """
        Change the application stylesheet
        """
        self.app.setStyleSheet(app_styles)
    
    def changePlayerBoard(self,fen):
        """
        Update the ChessPlayer Board
        """
        if (self.player is None):
            self.player = ChessPlayer(fen.replace("-","/")) #replace fen output for futher processing
        else:
            self.player.setBoard(fen.replace("-","/")) #replace fen output for futher processing

    def captureBoard(self):
        """
        Extract Board from the user's screen
        """
        img = get_screen_image(self.mainWindow)
        board_found , board_image = extract_board(img)
        if (board_found):
            fen = extract_fen(board_image)
            self.changePlayerBoard(fen)
            self.player.setOutBoard(board_image) #change the output board image
            self.player.startBoardConfig() #Open the board configuration window

        else:
            QMessageBox.warning(self.mainWindow, 'Chess Player - No Board Found', "Couldn't find a chess board from your screen.", QMessageBox.Ok, QMessageBox.Ok)

    def openSettings(self):
        """
        Open settings menu for potential modifications 
        """
        self.settingsManager.createUI()
        self.settingsManager.showUI()

    def showLastMove(self):
        """
        Retrieve the last image produced by the ChessPlayer
        """
        if self.player is not None and self.player.getLastMoveImage() is not None:
            cv2.imshow('Chess Player - The last move was',self.player.getLastMoveImage())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("You need to capture at least one board to show you the last move")
            msg.setWindowTitle("Chess Player - Nothing to show")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()


