from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
import chess
import chess.svg
from .keyEventHandler import *

symbols = "RNBKQP"


class BoardDrawer(QSvgWidget):
	"""
    Board Drawer Class
    """
	def __init__(self):
		super().__init__()
		self.selected_poistion = None
		self.board = None
		
	def setBoard(self, board):
		"""
        Update the board to show
        """
		self.board = board
		
	def mousePressEvent(self, event):
		"""
        Select/Unselect a clicked square on the board
        """
        #Get Square Size
		x = event.x()
		y = event.y()
		horz_sq_size = self.size().width() / 8
		vert_sq_size = self.size().height() / 8

        #Find Square Selected
		horz_index = int(x/horz_sq_size)
		vert_index = 7 - (int(y/vert_sq_size) % 8)
		horizontal_pos = chr(97 + horz_index)
		vertical_pos = str(vert_index)

        #Update selected square
		clicked_position = chess.square(horz_index, vert_index)
		if (self.selected_poistion != clicked_position):
			self.selected_poistion = clicked_position
			self.setFocus(True)
		else:
			self.setFocus(False)
			self.selected_poistion = None
		self.drawBoard()
	
	def keyPressEvent(self, event):
		"""
        Replace/Remove/Add a piece from/to the current selected square
        """
		sequence = keyevent_to_sequence(event)

		if (self.selected_poistion is not None):
			if (sequence[0] == "Backspace"):
				self.board.remove_piece_at(self.selected_poistion)
			if (sequence[0] == keymap[Qt.Key_Shift] and len(sequence) == 2):
				if (sequence[1] in symbols):
					piece = chess.Piece.from_symbol(sequence[1].lower())
					self.board.remove_piece_at(self.selected_poistion)
					self.board.set_piece_at(square=self.selected_poistion, piece=piece)
			elif(len(sequence) == 1 and sequence[0] in symbols):
				piece = chess.Piece.from_symbol(sequence[0])
				self.board.remove_piece_at(self.selected_poistion)
				self.board.set_piece_at(square=self.selected_poistion, piece=piece)
				
			self.drawBoard()

	def drawBoard(self):
		"""
        Draw the current board to the screen
        """
		assert(self.board != None)
		if self.selected_poistion is not None:
			chess_svg = chess.svg.board(board=self.board, size=400, coordinates=False, check=self.selected_poistion)
		else:
			chess_svg = chess.svg.board(board=self.board, size=400, coordinates=False)
	
		svg_bytes = bytearray(chess_svg, encoding='utf-8')
		self.renderer().load(svg_bytes)
