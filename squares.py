import pygame, sys, random
from pygame.locals import*
# imports library dependancies

import pdb
# imports the python debug module/library


###############################################
#########Defining the board & variable#########
###############################################
boardWidth = 4
# number of colums in the board
boardHeight = 4
# number of rows in the board
tileSize = 80
windowWidth = 640
windowHeight = 480
FPS = 30
Blank = None

# Defining the colors using R G B
black = (0, 0 , 0)
white = (255, 255, 255)
brightBlue = (0, 50, 255)
darkTurquoise = (3, 54, 73)
green = (0, 204, 0)

# Assigning the colors
BGCOLOR = darkTurquoise
tileColor = green
textColor = white
borderColor = brightBlue
BASICFONTSIZE = 20

buttonColor = white
buttonTextColor = black
messageColor = white

# Defining the margins of the board and tiles to fit within eachother
XMARGIN = int((windowWidth- (tileSize * boardWidth + (boardWidth - 1))) / 2)
YMARGIN = int((windowHeight - (tileSize * boardHeight + (boardHeight - 1))) / 2)
# tileSize * boardWidth gives you the sizing for the amount of tiles that can fit on your screen
# boardWidth - 1 gives you the boarder of the board
# wy is everything divided by 2?

# Keyboard controls
up = "up"
down = "down"
left = "left"
right = "right"

##############################
####Setting up the buttons####
##############################
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF,  NEW_RECT, SOLVE_SURF, SOLVE_RECT
    # setting global variables (now that I know this camelCase them next time)

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    # calls the clock method from library
    DISPLAYSURF = pygame.display.set_mode((windowWidth, windowHeight))
    # assigns the set_mode library to the windowWidth & windowHeight values
    # find out why, (guessing this library determines the dsplay and you bind it to your width and height)
    pygame.display.set_caption("Python Slider Puzzle Game Thingy")
    # call a library to set a caption that is outputted toteh display
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    ##############################################################
    ####Creating buttons & storing them in the options section####
    ##############################################################
    RESET_SURF, RESET_RECT = makeText("Reset", textColor, tileColor, windowWidth - 120, windowHeight - 90)
    # sets the text output, color, and positioning of  the reset button
    NEW_SURF, NEW_RECT = makeText("New Game", textColor, tileColor, windowWidth - 120, windowHeight - 60)
    # are these numbers in pixels??
    SOLVE_SURF, SOLVE_RECT = makeText("Solve", textColor, tileColor, windowWidth - 120, windowHeight - 30)

    mainBoard, soloutionSeq = generateNewPuzzle(80)
    solvedBoard = getStartingBoard()
    # assigns the solveBoard method to how the board is in it's starting state because it's hardcoded to be solved initially
    # the starting board is assigned to the win condition, this will be hard coded

    allMoves = []
    # stores an array of all moves made from the solved state
    # this is used to allow us to reverse the process for the solve configuration as oppose to programming an AI for solving

    while True:
    # main game loop
        slideTo = None
        # slides our tile to the blank variable we created earlier
        msg = "ELLO MOTO"
        # Creates a message in the  upper left hand corner
        if mainBoard == solvedBoard:
        # Our win condition!!!!
            msg = "You WIN!!!"

            drawBoard(mainBoard, msg)

            ########################
            ####Clicking Buttons####
            ########################
            checkForQuit()
            for event in pygame.event.get():
            #event handling loop that listens for a quit command
                if event.type == mouseButtonUp:
                # listens for the release of a button click
                    spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                    # recieves the coordinates from  the mouseButtonUp listener

                if (spotx, spoty) == (None, None):
                # listen for button clicks on main board
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves)
                        # onclick reset the board
                        allMoves = []

                    # THIS IS HOW YOU WRITE A ELSE IF STATEMENT IN PYTHON!!!
                    elif NEW_RECT.collidepoint(event.pos):
                            mainBoard, soloutionSeq = generateNewPuzzle(80)
                            # onclick generates new game and scrambles the board with 80 moves
                            allMoves = []

                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, soloutionSeq + allMoves)
                        # onclick soves the puzzle by taking all played moves and reversing them
                        allMoves = []

                    else:
                        # check if the clicked tile was next to a blank spot to

                        blankx, blanky = getBlankPosition(mainBoard)
                        if spotx == blankx + 1 and spoty == blanky:
                            slideTo = left
                        # if spot x & y coordinates are equal to the blank spot, slide the tile there
                        elif spotx == blankx - 1 and spoty == blanky:
                            slideTo = right
                        elif spotx == blankx and spoty == blanky + 1:
                            slideTo = right
                        elif spotx == blankx and spoty == blanky - 1:
                            slideTo = down

                        elif event.type == KEYUP:
                        # check to see if a key is released to check for keyboard directionals keypad
                            if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, left):
                                slideTo = left
                            elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, right):
                                slideTo = right
                            elif event.key in (K_UP, K_w) and isValidMove(mainBoard, up):
                                slideTo = up
                            elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, down):
                                slideTo = up

                        if slideTo:
                        # if the tile slides execture this ode block
                            slideAnimation(mainBoard, slideTo, "Click or press down to slde.", 8)
                            # display the slide on the screen
                            makeMove(mainBoard, slideTo)
                            allMoves.append(slideTo)
                            # records the slide for moves taken log
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)
                        # calls the imported library update function

def terminate():
    pygame.quit()
    sys.exit()
# terminate command to shut off program
# why is t being called here? is it to jump the loop?

def checkForQuit():
    for event in pygame.event.get(QUIT):
    # calls all the QUIT events
        terminate()
        # terminates the application if any of the QUIT conditions are method
    for event in pygame.event.get(KEYUP):
    # call all KEYUP events
        if event.key == K_ESCAPE:
            terminate()
            # activate terminate() if KEYUP event is for the ESC key
        pygame.event.post(event)
        # put the other KEYUP events back

def getStartingBoard():
# returns the board in it's starting state (solved state)
    counter = 1
    board = []
    for x in range(boardWidth):
    # this is how you write loops in Python
        column = []
        for y in range(boardHeight):
            column.append(counter)
            counter += boardWidth
        board.append(column)
        counter -= boardWidth * (boardHeight-1) + boardWidth - 1
        # loop through and log the tile moves to an array

    board[boardWidth - 1][boardHeight - 1] = None
    return board

def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(boardWidth):
        for y in range(boardHeight):
            if board[x][y] == Blank:
                return (x, y)

def getRandomMove(board, lastMove = None):
# start with full list of all four moves
    validMoves = [up, down, left, right]

    if lastMove == up or isValidMove(board, down):
        validMoves.remove(down)
    if lastMove == down or isValidMove(board, up):
        validMoves.remove(up)
    if lastMove == left or isValidMove(board, right):
        validMoves.remove(right)
    if lastMove == right or isValidMove(board, left):
        validMoves.remove(left)
    # this loop determines blank space movement

    return random.choice(validMoves)
# returns a random move from the list of remaining moves

def makeMove(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == up and blanky != len(board[0]) - 1) or \
           (move == down and blanky != 0) or \
           (move == left and blankx != len(board) - 1) or \
           (move == right and blankx != 0)

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * tileSize) + (tileX - 1)
    top = YMARGIN + (tileY * tileSize) + (tileY - 1)
    return(left, top)

def getSpotClicked(board, x, y):
# from the x & y pixel coordinates, get get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return(tileX, tileY)
    return(None, None)
    # I have no idea what this block of code does, need to look it up. REMEBER!!!


def drawTile(tilex, tiley, number, adjx = 0, adjy = 0):
# draw tile at coordinates tilex & tiley on te board, or optionally a few tiles over (determined by adjx & adjy)
# I am tired what des this do exactly? Find out
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, tileColor, (left + adjx, top + adjy, tileSize, tileSize))
    textSurf = BASICFONT.render(str(number), True, textColor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return(textSurf, textRect)

def makeText(text, color, bgcolor, top, left):
# creates the surface and Rect objects for some text
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return(textSurf, textRect)

def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])


    left, top = getLeftTopOfTile(0, 0)
    # assign coordinates 0, 0 to top left
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_RECT_SURF, SOLVE_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    if direction == up:
        movex = blankx
        movey = blanky + 1
    elif direction == down:
        movex = blankx
        movey = blanky - 1
    elif direction == left:
        movex = blankx + 1
        movey = blanky
    elif direction == right:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, tileSize, tileSize))

    for i in range(0, tileSize, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == up:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == down:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == left:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == right:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, messageColor, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = boardWidth * tileSize
    height = boardHeight * tileSize
    pygame.draw.rect(DISPLAYSURF, borderColor, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500) # pause 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(tileSize / 3)) # should this not be divided by 4?
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)

def resetAnimation(board, allMoves):
# reverse the all moves array that stores all previous moves enterd to solve puzzle
    revAllMoves = allMoves[:]
    #gets the copy of the array list
    revAllMoves.reverse()
    # reverses the array

    for move in revAllMoves:
    # function of the reverse() method
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, "", int(TILESIZE / 2))
        makeMove(board, oppositeMove)


if __name__ == "__main__":
    main()
