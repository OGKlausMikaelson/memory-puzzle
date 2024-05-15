import random, pygame, sys 
from pygame.locals import *

FPS =30 # frames per second, general speed of the program
WINDOWWIDTH = 640 # size of windows width in pixels
WINDOWHEIGHT = 480 # size of windows height in pixels
REVEALSPEED = 8 # SPEED OF BOXES REVEALING AND HIDING
BOXSIZE = 40 # size of box height and width in pixels
GAPSIZE = 10 # size of gaps btw boxes in pixels
BOARDWIDTH = 10 # number of columns of icons
BOARDHEIGHT = 7 # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board need to have an even number of boxes for pairs to match.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#           R    G    B
GRAY     =(100 ,100, 100)
NAVYBLUE =( 60 , 60, 100)
WHITE    =(255 ,255, 255)
RED      =(255 ,  0,   0)
GREEN    =(  0 ,255,   0)
BLUE     =(  0 ,  0, 255)
YELLOW   =(255 ,255,   0)
ORANGE   =(255 ,128,   0)
PURPLE   =(255 ,  0, 255)
CYAN     =(  0 ,255, 255)

BGCOLOR        = NAVYBLUE
LIGHTBGCOLOR   = GRAY
BOXCOLOR       = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT   = 'donut'
SQUARE  = 'square'
DIAMOND = 'diamond'
LINES   = 'lines'
OVAL    = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, BLUE, CYAN)
ALLSHAPES = (DONUT,SQUARE,DIAMOND,LIGHTBGCOLOR,OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDHEIGHT * BOARDWIDTH, "Board is too big for the number of shapes/colors defined."

def main() :
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(WINDOWWIDTH, WINDOWHEIGHT)

    mousex = 0  # use to store x coordinate of mouse event
    mousey = 0  # use to store y coordinate of mouse event
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x,y) of the first box revealed

    DISPLAYSURF.fill(BGCOLOR) #drawing the board
    startGameAnimation(mainBoard)

    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCLOR) # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE) :
                pygame.quit()
                sys.quit()
            elif event.type == MOUSEMOTION:
                mousex,mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex,mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex,mousey)
        if boxx!=None and boxy!=None:
            #the mouse pointer is over the box
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx,boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked :
                revealBoxesAnimation(mainBoard,[boxx,boxy])
                revealedBoxes[boxx][boxy] = True #set the box as revealed
                if firstSelection == 'None' : #the current box was the first box clicked
                    firstSelection = (boxx,boxy)
                else: # the current box clicked was the second box clicked
                    #check if the second clicked box matches the first
                    icon1shape, icon1color = getShapeAndColor(mainBoard,firstSelection[0],firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard,boxx,boxy)

                    if icon1color != icon2color or icon1shape != icon2shape :
                        # icons dont match recover both selected boxes
                        pygame.time.wait(1000) #1000ms = 1 sec
                        coverBoxesAnimation(mainBoard,[(firstSelection[0],firstSelection[1]),(boxx,boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes) : #check if all pairs found
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        #Reset the board 
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        #Show the fully unrevealed board for a second
                        drawBoard(mainBoard,revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        #Replay the start game animation
                        startGameAnimation(mainBoard)
                    firstSelection = None # reset first selection variable
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val]*BOARDHEIGHT)
    return revealedBoxes

def getRandomizedBoard():
    # get a list of all possible shape in every possible order
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((color,shape))
    random.shuffle(icons)

    #Create board data structure , with rabdomly placed icons
    
                


         

