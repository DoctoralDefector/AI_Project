# Reversi
import random
import sys
import time

takeTime = 0
def drawBoard(board):
    # This function prints out the board that it was passed. Returns None.
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(HLINE)

    for y in range(8):
        print(VLINE)
        print(y + 1, end=' ')

        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')

        print('|')
        print(VLINE)
        print(HLINE)


def resetBoard(board):
    # Blanks out the board it is passed, except f7or the original starting position.
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    # Starting pieces:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


def getNewBoard():
    # Creates a brand new, blank board data structure.
    board = []
    for i in range(8):
        board.append([' '] * 8)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile  # temporarily set the tile on the board.
    if tile == 'X':
        otherTile = 'O'

    else:
        otherTile = 'X'

    tilesToFlip = []

    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection  # first step in the direction
        y += ydirection  # first step in the direction

        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection

            if not isOnBoard(x, y):
                continue

            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection

                if not isOnBoard(x, y):  # break out of while loop, then continue in for loop
                    break

            if not isOnBoard(x, y):
                continue

            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection

                    if x == xstart and y == ystart:
                        break

                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' '  # restore the empty space

    if len(tilesToFlip) == 0:  # If no tiles were flipped, this is not a valid move.
        return False

    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


def getBoardWithValidMoves(board, tile):
    # Returns a new board with . marking the valid moves the given player can make.
    dupeBoard = getBoardCopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'

    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])

    return validMoves


def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.

    xscore = 0
    oscore = 0

    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1

            if board[x][y] == 'O':
                oscore += 1

    return {'X': xscore, 'O': oscore}


def enterPlayerTile():
    # Lets the player type which tile they want to be.
    # Returns a list with the player's tile as the first item, and the computer's tile as the second.
    tile = ''

    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()
    # the first element in the list is the player's tile, the second is the computer's tile.

    if tile == 'X':
        return ['X', 'O']

    else:
        return ['O', 'X']


def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'

    else:
        return 'player'


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile

    for x, y in tilesToFlip:
        board[x][y] = tile

    return True


def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getPlayerMove(board, playerTile):
    # Let the player type in their move.
    # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
        move = input().lower()

        if move == 'quit':
            return 'quit'

        if move == 'hints':
            return 'hints'

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1

            if isValidMove(board, playerTile, x, y) == False:
                continue

            else:
                break

        else:
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81 will be the top-right corner.')

    return [x, y]

def alphabeta(board, computerTile, playerTile, isComputer, depth, alpha, beta, count):
    global takeTime
    start_time = time.time()
    possibleMoves = getValidMoves(board, computerTile)
    if len(possibleMoves) == 0 or depth == 0:
        if isComputer:
            takeTime += time.time() -start_time
            return heuristic(board, computerTile), count + 1, None
        takeTime += time.time() -start_time
        return heuristic(board, playerTile), count + 1, None
    #max player
    if isComputer:
        best = -8000
        for x, y in possibleMoves:
            dupeBoard = getBoardCopy(board)
            makeMove(dupeBoard, computerTile, x, y)
            score, count, _ = alphabeta(board, computerTile, playerTile, 0, depth - 1, alpha, beta, count)

            if score > best:
                bestMove = [x, y]
                best = score
            if alpha < best:  # alpha becomes max of best and alpha
                alpha = best
            if alpha >= beta:  # beta <= parent alpha then break

                takeTime += time.time() -start_time
                break
                # BREAK BETA
    else:
        best = 8000
        for x, y in possibleMoves:
            dupeBoard = getBoardCopy(board)
            makeMove(dupeBoard, computerTile, x, y)
            score, count, _ = alphabeta(board, computerTile, playerTile, 0, depth - 1, alpha, beta, count)

            if score < best:
                bestMove = [x, y]
                best = score
            if beta > best:  # alpha becomes max of best and alpha
                alpha = best
            if alpha >= beta:  # beta <= parent alpha then break
                takeTime += time.time() -start_time
                break
                # BREAK BETA
    takeTime += time.time() -start_time
    return best, count + 1, bestMove

def heuristic(board, ownerTile):
    #100 assigned per corner, then score is number of tiles - opponent tiles
    score = 0
    corners = [[0,0],[0,7],[7,0],[7,7]]
    for x, y in corners:
        if board[x][y] == ownerTile:
            score += 100
        else:
            if (ownerTile == 'X' and board[x][y] == 'O') or (ownerTile == 'O' and board[x][y] == 'X'):
                score += -100
    score += getScoreOfBoard(board)[ownerTile]
    return score


def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    if computerTile == 'X':
        playerTile == 'O'
    else:
        playerTile == 'X'
    global takeTime
    takeTime = 0
    _, count, bestMove = alphabeta(board, computerTile, playerTile, 1, 5, -9000, 9000, 0)
    print("How long did it take? >> "+str(takeTime))

    print('Count: ', count)
    return bestMove


def getComputerMoveNoAB(board, computerTile):
    #AB stands for Alpha Beta, among other things
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)
    # randomize the order of the possible moves
    random.shuffle(possibleMoves)
    # always go for a corner if available.

    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    # Go through all the possible moves and remember the best scoring move
    bestScore = -1

    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]

        if score > bestScore:
            bestMove = [x, y]
            bestScore = score

    return bestMove



def showPoints(playerTile, computerTile):
    # Prints out the current score.
    scores = getScoreOfBoard(mainBoard)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))


print('Welcome to Reversi!')

while True:
    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')

    while True:
        if turn == 'player':
            # Player's turn.
            if showHints:
                validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                drawBoard(validMovesBoard)

            else:
                drawBoard(mainBoard)

            showPoints(playerTile, computerTile)
            move = getPlayerMove(mainBoard, playerTile)

            if move == 'quit':
                print('Thanks for playing!')
                sys.exit()  # terminate the program

            elif move == 'hints':
                showHints = not showHints
                continue

            else:
                makeMove(mainBoard, playerTile, move[0], move[1])

            if getValidMoves(mainBoard, computerTile) == []:

                break

            else:
                turn = 'computer'

        else:
            # Computer's turn.
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            input('Press Enter to see the computer\'s move.')
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y)

            if getValidMoves(mainBoard, playerTile) == []:
                break

            else:
                turn = 'player'

    # Display the final score.

    drawBoard(mainBoard)

    scores = getScoreOfBoard(mainBoard)
    print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))

    if scores[playerTile] > scores[computerTile]:
        print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))

    elif scores[playerTile] < scores[computerTile]:
        print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))

    else:
        print('The game was a tie!')

    if not playAgain():
        break