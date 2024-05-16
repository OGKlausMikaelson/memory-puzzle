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
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as soons as we assign them
        board.append(column)
    return (board)

def splitIntoGroupsOf(groupSize,theList):
    #splits a list into a list of lists, where the inner list have at
    # most groupSize number of items.
    result = []
    for i in range(0,len(theList),groupSize):
        result.append(theList[i:i + groupSize])
    return result

def letTopCoordsOfBox(boxx,boxy):
    #convert box coordinates to pixels coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    right = boxy* (BOXSIZE + GAPSIZE) + YMARGIN
    return (left,right)

def getBoxAtPixel(x,y):
    for boxx in range(BOARDWIDTH):
         for boxy in range(BOARDHEIGHT):
             left,top=leftTopCoordsOfBox(boxx,boxy)
             boxRect = pygame.Rect(left,top,BOXSIZE,BOXSIZE)
             if boxRect.collidepoint(x,y):
                 return (boxx,boxy)
    return (None,None)

def drawIcon(shape,color,boxx,boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half    = int(BOXSIZE * 0.50) # Ssyntatic sugar

    left, top = leftTopCoordOfBox(boxx,boxy) # get pixels coords from board coordinates
    # Draw the shape
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left+half,top+half),half-5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left+half,top+half),quarter-5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top+quarter, BOXSIZE-half,BOXSIZE-half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left+half,top),(left+BOXSIZE-1,top+half),(left+half,top+BOXSIZE-1), (left, top+half)))

    elif shape == LINES:
        for i in range(0,BOXSIZE,4):
            pygame.draw.line(DISPLAYSURF, color, (left, top+i), (left+i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i,top+BOXSIZE-1),(left+BOXSIZE-1,top+i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF,color, (left,top+quarter,BOXSIZE,half))

def getShapeAndColor(board, boxx, boxy):
    #shape value for x, y is stored in board[x][y][0]
    #color value for x,y is stored in board [x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    #Draw boxes being covered/revealed. "boxes" is a list.
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left,top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage>0: # draw the coverage if there is a coverage
            pygame.draw.rect(DISPLAYSURF,BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board,boxesToReveal):
    #Do the box "reveal" animation
    for coverage in range(BOXSIZE, (-REVEALSPEED)-1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    #Do the box "cover" animation
    for coverage in range(0,BOXSIZE+REVEALSPEED,REVEALSPEED):
        drawBoxCovers(board,coverBoxesAnimation,coverage)

def drawBoard(board,revealed):
    # Draw all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = letTopCoordsOfBox(boxx,boxy)
            if not revealed[boxx][boxy]:
                # draw a covered box
                pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board,boxx,boxy)
                drawIcon(shape,color,boxx,boxy)

def drawHighlightBox(boxx,boxy):
    left,top = letTopCoordsOfBox(boxx,boxy)
    pygame.draw.rect(DISPLAYSURF,HIGHLIGHTCOLOR, (left-5,top-5,BOXSIZE+10, BOXSIZE+10),4)


def startGameAnimation(board):
    #Randomnly reveal boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8,boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board,boxGroup)
        coverBoxesAnimation(board,boxGroup)

def gameWonAnimation(board):
    # flash the bg color when player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1,color2 = color2,color1 # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board,coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    # true if all boxes have been revealed else false
    for i in revealedBoxes:
        if False in i:
            return False #return False if any of the boxes are covered
    return False

if __name__ == '__main__':
    main()
    
    
                


         

