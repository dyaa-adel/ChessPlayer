from keras.models import load_model
from skimage.transform import resize
from skimage.util.shape import view_as_blocks
import os

SQUARE_SIZE = 40 #must be less than 400/8==50
MODEL_PATH = os.path.join(os.path.dirname(__file__), "piece_recognition.hdf5")
model = load_model(MODEL_PATH , compile=False) #load piece recogniser
piece_symbols = 'prbnkqPRBNKQ' #Symbols used in the fen notation

def process_image(img_read):
    """
    Process the extracted board (Downsampling - Squares Extractions)
    """
    downsample_size = SQUARE_SIZE*8
    square_size = SQUARE_SIZE
    img_read = resize(img_read, (downsample_size, downsample_size), mode='constant')
    tiles = view_as_blocks(img_read, block_shape=(square_size, square_size, 3))
    tiles = tiles.squeeze(axis=2)
    return tiles.reshape(64, square_size, square_size, 3)

def fen_from_onehot(one_hot):
    """
    Convert from onehot encoding to FEN notation
    """
    output = ''
    for j in range(8):
        for i in range(8):
            if(one_hot[j][i] == 12):
                output += ' '
            else:
                output += piece_symbols[one_hot[j][i]]
        if(j != 7):
            output += '-'

    for i in range(8, 0, -1):
        output = output.replace(' ' * i, str(i))

    return output
    
def extract_fen(image):
    """
    Return fen notation given an extracted board image
    """
    pred = model.predict(process_image(image)).argmax(axis=1).reshape(-1, 8, 8)
    fen = fen_from_onehot(pred[0])
    return fen

