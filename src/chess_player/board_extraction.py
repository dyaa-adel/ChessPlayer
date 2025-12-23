from numpy import pi
import cv2 
from .board_state_utils import SQUARE_SIZE

def add_boundaries(board_width,h,v,error): 
	"""
    Add horizontal and vertical lines to the boundary of the extracted board
    """
	if not (h[0][0] < error):
		h.insert(0,[1.,h[0][1]])
	h[0][0] = 1
	if not (h[-1][0] > board_width -  error):
		h.append([board_width,h[-1][1]])
	h[-1][0] = board_width
	if not (v[0][0] < error):
		v.insert(0,[1.,v[0][1]])
	v[0][0] = 1

	if not (v[-1][0] > board_width -  error):
		v.append([board_width,v[-1][1]])
	v[-1][0] = board_width

	return h , v

def hor_vert_lines(lines):
	"""
	A line is given by rho and theta. Given a list of lines, returns a list of
	horizontal lines (theta=90 deg) and a list of vertical lines (theta=0 deg).
	"""
	h = []
	v = []
	for line in lines:
		for distance, angle in line:
			if angle < pi / 4 or angle > pi - pi / 4:
				v.append([distance, angle])
			else:
				h.append([distance, angle])
	h.sort(key = lambda x : x[0])
	v.sort(key = lambda x : x[0])
	return h, v


def sort_cnts(cnt):
	"""
    Used for sorting an array of contours based on the their width
    """
	x,y,w,h = cv2.boundingRect(cnt)
	return w

def get_largest_sq(binary):
	"""
    Retrun the largest square object found in the given binary Image
	And it should be the chess board
    """
	#Image Processing to connect board checker pattern for contour extraction
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
	binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
	binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
	####Modification of image due to chess board borders####
	binary = cv2.Canny(binary,50,150,apertureSize = 3)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
	binary = cv2.dilate(binary,kernel,iterations = 1)
	####Modification of image due to chess board borders####

	#Find All Contours
	# cnts = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Doesn't work if there was larger border
	cnts = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
	
	
	#Retrieve only the square contours with an error of {error}
	sq_cnts = []
	error = 5
	for c in cnts:
		x,y,w,h = cv2.boundingRect(c)
		if abs(w - h) < error:
			sq_cnts.append(c)
	
	#Sort the square contours to retrieve the largest square contour 
	if sq_cnts:
		sq_cnts.sort(key=sort_cnts,reverse=True)
		x,y,w,h = cv2.boundingRect(sq_cnts[0])
		return x,y,w,h
	
	else:
		return 0 ,0 , 0 , 0
		

def get_board_image(color):
	"""
    Return the extracted largest squared contour from a given image 
    """
	#Color to grey
	grey = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)

	#Apply both threshold modes to determine which one produces the largest square
	ret,img1 = cv2.threshold(grey,150,255,cv2.THRESH_BINARY)
	ret,img2 = cv2.threshold(grey,150,255,cv2.THRESH_BINARY_INV)

	#Retrieve largest squares for both modes
	x1,y1,w1,h1 = get_largest_sq(img1)
	x2,y2,w2,h2 = get_largest_sq(img2)


	print('w1 : ',w1)
	print('w2 : ',w2)

	#No Sqaures found
	if (w1 == 0) and (w2 == 0):
		return False , False


	if w1 > w2 : #Find which mode INV or NOT INV detected the largest square
		grey_image = grey[y1:y1+h1, x1:x1+w1]
		color_image = color[y1:y1+h1, x1:x1+w1]
	else:
		grey_image = grey[y2:y2+h2, x2:x2+w2]
		color_image = color[y2:y2+h2, x2:x2+w2]
	
	return grey_image,color_image

def extract_pattern(board,h,v):
	"""
    Check if the chess board patter found in the extracted square 
	and return the square that matched pattern only removing redundant pixels
    """
	error = 5
	horz_pattern = False
	vert_pattern = False
	board_found = False

	#Check horizontal pattern
	spacing = 5000
	starting_h = 0
	checkers_found = 1
	for index in range(0,len(h)-1):
		if abs (h[index+1][0]-h[index][0] - spacing) > error:
			starting_h = index
			checkers_found = 1
			spacing = h[index+1][0]-h[index][0]
		else:
			checkers_found = checkers_found + 1
		if checkers_found == 8:
			print('Horizontal pattern found')
			horz_pattern = True
			break
		
	#Check vertical pattern
	spacing = 5000
	starting_v = 0
	checkers_found = 1
	for index in range(0,len(v)-1):
		if abs (v[index+1][0]-v[index][0] - spacing) > error:
			starting_v = index
			checkers_found = 1
			spacing = v[index+1][0]-v[index][0]
		else:
			checkers_found = checkers_found + 1
		if checkers_found == 8:
			print('Vertical pattern found')
			vert_pattern = True
			break
	
	#Is Horizontal and Vertical Patterns Found 
	if vert_pattern and horz_pattern:
		board_found = True
		board = board[int(h[starting_h][0]):int(h[starting_h + 8][0]),int(v[starting_v][0]):int(v[starting_v + 8][0])]
		
		return board_found , board
	else:
		return board_found , []

def extract_board(img):
	"""
    Given a screenshot image from the user , extract a chess board if found
    """
	#Get largest square in the image
	grey_board , color_board = get_board_image(img)

	#Check if a sqaure was found
	if color_board is False:
		print("Not Square")
		return False , None

	#Check if the size is at least the acceptable board size
	#TODO Scale up the image a bit if it was close to the min size
	if color_board.shape[0] < SQUARE_SIZE * 8:
		print("Not good size")
		return False , None

	#Get hough lines from the extracted square
	img_e = cv2.Canny(grey_board,50,150,apertureSize = 3)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
	img_e = cv2.dilate(img_e,kernel,iterations = 1)
	lines = cv2.HoughLines(img_e,1,pi/180,int(3/4 * len(color_board)))

	#Get horz and vert lines to check the pattern
	h, v = hor_vert_lines(lines)
	h, v = add_boundaries(len(color_board),h,v,5)

	#Extract the pattern
	board_found , ex_board  = extract_pattern(color_board,h,v)

	if board_found:
		color_board = ex_board
		return board_found , color_board

	else:
		return board_found , None
