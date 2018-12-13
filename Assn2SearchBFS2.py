'''

BFS Search untill destination point is reached. 

This code implements the generic search algorithm:

Insert the given start state into the READY ADT
REPEAT
	Remove a state from the READY ADT.
	Place that state into a variable current_state
	Insert that state into the VISITED ADT. 
	IF (the current state is the terminal state) THEN finished!
	FOR (each neighbor of current_state in NEITHER)
		Insert that neighbor state into READY
	ENDFOR

UNTIL the terminal state is encountered

'''
import heapq
import time  # for pause during graphic display

START_X = 350 # HARDCODED  Start X coordinate of search path
START_Y = 130 # HARDCODED  Start Y coordinate of search path
GOAL_X = 30 # HARDCODED  Goal X coordinate of search path
GOAL_Y = 300 # HARDCODED  Goal Y coordinate of search path
STEP_SIZE = 10 # HARDCODED   Number of pixels at each search step (separation of neighbors)
IMAGE_WIDTH = 500 # HARDCODED   Image width in pixels
IMAGE_HEIGHT = 500 # HARDCODED   Image height in pixels
currentPriority = 0 # Initialize to a "low" (sooner returned) priority for pri. queue
# loopCounter = 5000

# Use PILLOW to read data from within image, but not to display image or graphically show path.
# This is because PILLOW displays the image using the "operating-system default application," such
# as MS Paint, IrfanView, etc., and it's not possible to annotate that graphic by displaying
# graphics primitives within that graphic default application.
from PIL import Image
PILimg = Image.open('JeffersonNickel500.png') # Valid file types: bmp, ppm, jpg, png, gif
#PILimg.show()  # Uses the selected image application (MS Paint, IrfanView, etc.)

# pixel access   https://pillow.readthedocs.io/en/5.2.x/reference/PixelAccess.html
px = PILimg.load()  # px is an object of class PixelAccess

'''
# Demo of two ways of obtaining RGB at a selected point as a three-component tuple
print (px[4,4])
myPixel = PILimg.getpixel((4, 4))   
print (myPixel)
'''

# Use tkinter to display image and graphically show path, but not read data from within image
# This version is GIF or PPM file
from tkinter import *      
root = Tk()      
canvas = Canvas(root, width = IMAGE_WIDTH, height = IMAGE_HEIGHT)   
canvas.pack()      
TKimg = PhotoImage(file="JeffersonNickel500.png")  # Valid file types: ppm, png file, NOT GIF, BMP, JPG
canvas.create_image(0,0, anchor=NW, image=TKimg)
# canvas.create_line(10, 10, 100, 100)

def elevation(x, y):
	# PILimg.getpixel((x, y)) returns a "triplet" tuple that is the (R, G, B) value. 
	# We need a single "elevation" value from the triplet (R, G, B).
	# In a grayscale image, R == G == B, so return only one of the components.
	#print("The three-component RGB tuple is ", PILimg.getpixel((x, y))) 
	#print("  --- but I really want only the first component, ", (PILimg.getpixel((x, y)))[0]) 
	return (PILimg.getpixel((x, y)))[0]  # Only the first of the three-component RGB tuple

# Determine the priority (evaluation) of the state.
# The priority of a state is the sum of:
#   Known distance from initial state to current state
#     plus
#   Estimated cost from current state to goal state
def priority(cx, cy):  # (cx, cy) is the coordinate of the Current state

	global currentPriority   # Declare "currentPriority" as a global variable

	# knownCostToCurrent = abs(elevation(START_X, START_Y) - elevation(cx, cy))
	# estimCostToGoal = abs(elevation(GOAL_X, GOAL_Y) - elevation(cx, cy))
	# return (knownCostToCurrent + estimCostToGoal)
	
	'''
	# Breadth-first search -- priority increases every time an element
	# is inserted into the priority queue.'''
	
	# global currentPriority   # Declare "currentPriority" as a global variable
	# Each call of this function, priority() results in an INCREASED VALUE of priority
	currentPriority += 1
	return currentPriority
	

# The "state" is a tuple of the form (priority [x,  y])
# The "priority queue" is a list of "state" tuples, where the lowest-priority
# state is at the front and all other states in the "priority queue" are un-ordered

# CURRENT_STATE = [(priority(START_X, START_Y), [START_X, START_Y])]   # Start location
# print (CURRENT_STATE)
#print("CURRENT_STATE is ", CURRENT_STATE)

READY = [(priority(START_X, START_Y), [START_X, START_Y])]   # Start location
# Transform list READY into heap.

heapq.heapify(READY) 


VISITED = []  # Initialize to empty list

# Limit number of loops during development
# loopCounter = 1000

while True:  # Infinite loop, must be break-ed out of
	CURRENT_STATE = heapq.heappop(READY)  # Current location
	
	
	# CURRENT_STATE[1][0] is the X coordinate of the current state, and
	# CURRENT_STATE[1][1] is the Y coordinate of the current state.
	canvas.create_oval(CURRENT_STATE[1][0]-2, CURRENT_STATE[1][1]-2,   # HARDCODED CIRCLE SIZE
		CURRENT_STATE[1][0]+2, CURRENT_STATE[1][1]+2,
		fill='red', outline='red')
	canvas.update()
	# time.sleep(.3) # HARDCODED
	
	heapq.heappush(VISITED, CURRENT_STATE)
	
	# IF (the current state is the terminal state) THEN finished!
	# CURRENT_STATE[1][0] is the X coordinate of the current state, and
	# CURRENT_STATE[1][1] is the Y coordinate of the current state.
	if CURRENT_STATE[1][0] == GOAL_X and CURRENT_STATE[1][1] == GOAL_Y:
		print("\n\n GOAL state (", CURRENT_STATE )
		canvas.create_oval(CURRENT_STATE[1][0]-2, CURRENT_STATE[1][1]-2,   # HARDCODED CIRCLE SIZE
			CURRENT_STATE[1][0]+2, CURRENT_STATE[1][1]+2,
			fill='black', outline='black')
		break  # We've reached the goal state; no further search
	
	
	'''
	FOR (each neighbor of current_state that is not in READY nor in VISITED)
		heapq.heappush(READY, NEIGHBOR)  # Insert that neighbor state into READY
	
	CURRENT_STATE[1][0] is the X coordinate of the current state, and
	CURRENT_STATE[1][1] is the Y coordinate of the current state.
	'''
	for nx in range(CURRENT_STATE[1][0] - 10, CURRENT_STATE[1][0] + 10 + 1, 10):
		for ny in range(CURRENT_STATE[1][1] - 10, CURRENT_STATE[1][1] + 10 + 1, 10):
		
			if (nx < 0 or ny < 0 or nx >= IMAGE_WIDTH or ny >= IMAGE_HEIGHT):
				continue  # don't allow a "neighbor" to be out of bounds

			if (nx == CURRENT_STATE[1][0] and ny == CURRENT_STATE[1][1]):
				continue  # don't allow a "neighbor" to duplicate the current state
				
			# if the state (nx, ny) is in VISITED or READY, don't re-visit or re-insert into READY
			if (priority(nx, ny), [nx, ny]) in VISITED:
				#print("state (", nx, ",", ny, ") is in VISITED" )
				continue
			if (priority(nx, ny), [nx, ny]) in READY:
				#print("state (", nx, ",", ny, ") is in READY" )
				continue

		
			#print("A valid neighbor position is    ", nx, " and ", ny)
			
			heapq.heappush(READY, (priority(nx, ny), [nx, ny]) )  # Insert each neighbor state into READY
	
	
	
	# Limit number of loops during development
	# loopCounter = loopCounter - 1
	# if loopCounter <= 0:
	# 	break


mainloop()   # Graphics loop -- This statement follows all other statements
