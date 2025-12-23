from PyQt5.QtWidgets import QMessageBox
from .configureBoardWindow import *
from .SettingsManager import *
import os
import chess.engine
from chess import flip_horizontal , flip_vertical
from .show_move import *

def show_no_engine_msgbox():
    """
    Show no chess engine found message box
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText("Couldn't find the chess engine in the specified file.")
    msg.setWindowTitle('Chess Player - No Chess Engine')
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


def get_engine_path():
    """
    Return the engine path found in settings
    """
    return SettingsManager().get_settings()["Engine Path"]

class ChessPlayer:
    """
    Chess Player Class
    """
    def __init__(self,fen):
        super().__init__()
        self.selected_poistion = None
        self.board = chess.Board(fen)  
        self.window = None
        self.last_move_image = None
        

    def changeTurns(self,current_unit,current_layout):
        """
        Modify the board for the next turn to be the chosen unit from the user
        """
        if (current_layout == 'White top'):
            self.board = self.board.mirror()
            self.board = self.board.transform(chess.flip_vertical)
            # self.board = self.board.transform(chess.flip_horizontal)
            
            current_epd = self.board.epd().split(' ')
            print(current_epd)
            current_epd[1] = current_unit[0].lower()
            if (current_epd[1] == 'w'):
                current_epd[1] = 'b'
            else:
                current_epd[1] = 'w'

        else:
            current_epd = self.board.epd().split(' ')
            current_epd[1] = current_unit[0].lower()
            print("White bottom")

        self.board.set_epd(' '.join(current_epd))
        print( self.board.fen() )
        self.window.updateBoard(self.board)

    def setBoard(self,fen):
        """
        Set the board to be used by the chess engine from FEN notation
        """
        self.board = chess.Board(fen)

    def getNextMove(self,current_unit,current_layout): 
        """
        Run the chess engine with UCI communication to find the next move to draw for the user
        """
        print('Next move for ' + current_unit)
        if (not self.board.is_checkmate()): #TODO add a you already won message and hooray ceremony if winning
            try:
                engine = chess.engine.SimpleEngine.popen_uci(get_engine_path())
                # current_turn = self.board.epd().split(' ')[1]
                self.changeTurns(current_unit,current_layout)
                user_time_limit = int(SettingsManager().settings["Engine Time Limit"])    
                #TODO check if game finished , as it crashes the engine
                result = engine.play(self.board, chess.engine.Limit(time=user_time_limit)) 
                print(result)
                self.board.push(result.move)
                self.last_move_image = show_move(str(result.move),self.out_board)
                self.window.updateBoard(self.board)
                engine.close()
                self.window.close()
            except OSError:
                print("Couldn't find your chess player")
                show_no_engine_msgbox()
    

    
    def startBoardConfig(self):
        """
        Instantiate Configure Board Window
        """
        self.window = ConfigueBoardWindow(self.board)
        self.window.getNextButton().clicked.connect(lambda: self.getNextMove(self.window.getUnitSelected() , self.window.getLayoutSelected()))

    def setOutBoard(self,out_board):
        """
        Update the output board 
        """
        self.out_board = out_board

    def getLastMoveImage(self):
        """
        Return the output board with the move highlighted to the caller
        """
        return self.last_move_image