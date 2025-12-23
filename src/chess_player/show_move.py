from cv2 import arrowedLine
from cv2 import imshow
from .SettingsManager import *

board_with_move = None

def move_to_index(move):
    """
    Given a chess move notation return from and to coordinates
    """
    from_p = move[0]+move[1]
    to_p = move[2] + move[3]
    from_x = ord(from_p[0]) - 97
    from_y = 8 - int(from_p[1]) #We do this because the image coordinates starts fro top-left corner
    to_x = ord(to_p[0]) - 97
    to_y = 8 - int(to_p[1]) #We do this because the image coordinates starts fro top-left corner
    return ( (from_x,from_y) , (to_x, to_y))


def get_point(squares_index,square_size):
    x = squares_index[0] * square_size + int(square_size/2)
    y = squares_index[1] * square_size + int(square_size/2)
    return (x,y)

def show_move(move,out_board):
    """
    Given chess move notation and the output board , 
    draw an arrow representing the move on the board
    and return the modified board to the caller
    """
    global board_with_move
    squares_indices = move_to_index(move)
    square_size = int(out_board.shape[1] / 8)

    from_point = get_point(squares_indices[0],square_size)
    to_point = get_point(squares_indices[1],square_size)

    print(from_point)
    print(to_point)
    arr_thick = int(SettingsManager().get_settings()["Arrow Thickness"])
    arr_color = SettingsManager().get_settings()["Arrow Color"].lstrip("#")
    arr_color = tuple(int(arr_color[i:i+2], 16) for i in (0, 2, 4))[::-1]
    
    arrowedLine(out_board,from_point,to_point,arr_color, thickness=arr_thick) 
    imshow('Chess Player - Here is your next move',out_board)
    return out_board