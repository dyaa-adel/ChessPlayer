from PyQt5.QtWidgets import QApplication , QLabel , QWidget , QPushButton , QHBoxLayout , QVBoxLayout , QComboBox
from .BoardDrawer import *

def create_unit_comboBox():
    cb = QComboBox()
    cb.addItem('Black')
    cb.addItem('White')
    return cb

def create_unit_selection_layout(unit_cb):
    h_layout = QHBoxLayout()
    h_layout.addWidget(QLabel("Whats is your unit ?"))
    h_layout.addWidget(unit_cb)

    return h_layout

def create_layout_comboBox():
    cb = QComboBox()
    cb.addItem('White bottom')
    cb.addItem('White top')
    return cb

def create_layout_selection_layout(unit_cb):
    h_layout = QHBoxLayout()
    h_layout.addWidget(QLabel("Whats is your board layout ?"))
    h_layout.addWidget(unit_cb)

    return h_layout

class ConfigueBoardWindow(QWidget):
    """
    Configure Board Window Class
    """
    def __init__(self,board):
        super().__init__()
        self.setObjectName('window')
        self.setWindowTitle("Chess Player - Configure Board")

        #Instantiate BoardDrawer
        self.boardDrawer = BoardDrawer()
        self.board = board

        #Configure Window
        self.boardDrawer.setGeometry(400,400,400,400)
        self.boardDrawer.setBoard(board)
        self.boardDrawer.drawBoard()

        #Window main layout
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        #Top
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.boardDrawer)

        #Bottom
        self.unit_comboBox = create_unit_comboBox()
        self.layout_comboBox = create_layout_comboBox()

        unit_selection_layout = create_unit_selection_layout(self.unit_comboBox)
        layout_selection_layout = create_layout_selection_layout(self.layout_comboBox)
        self.next_button = QPushButton("Show me the next move")
        v_layout.addLayout(unit_selection_layout)
        v_layout.addLayout(layout_selection_layout)

        v_layout.addWidget(self.next_button)

        self.setLayout(v_layout)
        self.setFixedSize(self.sizeHint()) #Disable resize
        self.show()
	
    def getNextButton(self):
        """
        Return the 'Show me next move' button
        """
        return self.next_button

    def getUnitSelected(self):
        """
        Return the selected unit from the combo box
        """
        return self.unit_comboBox.currentText()
    
    def getLayoutSelected(self):
        """
        Return the selected unit from the combo box
        """
        return self.layout_comboBox.currentText()
    
    def updateBoard(self,board):
        """
        Update current board for self and BoardDrawer instance
        """
        self.board = board
        self.boardDrawer.setBoard(board)
        self.boardDrawer.drawBoard()