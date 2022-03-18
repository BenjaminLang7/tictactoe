import random
from flask import flash, session

board = []

def createBoard():
    for i in range(9):
        board.append('-')
    return board

def playerTurn():
    #Validation logic to ensure user input can be processed#
    run = True
    while run:
        turn = input('Please provide a position (0 through 8) to mark X: ')
        try:
            turn = int(turn)
            #Above ensures they provide an actual number#
            if turn > -1 and turn < 9:
                if spotOpen(turn):
                    run = False
                    makeMove(turn, 'X')
                else:
                    print("This spot is already taken")
            else:
                print('Please provide a number between 0 and 8, that is not an occupied space')
        except:
            print('Please provide a number between 0 and 8, that is not an occupied space')
            #Above ensures they provide an actual number assuming the try failed#


def aiTurn():
    possibleMoves = [x for x, mark in enumerate(board) if mark == '-']
    #Above will number all "spaces" within the board list for ID.#
    move = -1
    #Check a copy of the board for possible wins that are one move away, starting with O
    for mark in ['O', 'X']:
        for i in possibleMoves:
            boardState = board[:]
            boardState[i] = mark
            if win(boardState, mark):
                move = i
                return move
    #Check to see if a corner is available, and if so, move into a random corner#
    cornersAvailable = []
    for i in possibleMoves:
        if i in [0,2,6,8]:
            cornersAvailable.append(i)
    if len(cornersAvailable) > 0:
        move = selectRandom(cornersAvailable)
        return move
    #Check to see if the middle is open, and if so, move into the middle
    if 4 in possibleMoves:
        move = 4
        return move
    #Finally, AI will default to a random edge#
    edgesAvailable = []
    for i in possibleMoves:
        if i in [1,3,5,7]:
            edgesAvailable.append(i)
    if len(edgesAvailable) > 0:
        move = selectRandom(cornersAvailable)
        return move

def selectRandom(possibilities):
    length = len(possibilities)
    r = random.randrange(0,length)
    return possibilities[r]

def makeMove(position, mark):
    board[position] = mark

def win(board, mark):
    # Games ends with a winner if we see one of the 8 different possible ways to win#
    if (board[0] == mark and board[1] == mark and board[2] == mark) or (board[3] == mark and board[4] == mark and board[5] == mark) or (board[6] == mark and board[7] == mark and board[8] == mark) or (board[0] == mark and board[3] == mark and board[6] == mark) or (board[1] == mark and board[4] == mark and board[7] == mark) or (board[2] == mark and board[5] == mark and board[8] == mark) or (board[0] == mark and board[4] == mark and board[8] == mark) or (board[6] == mark and board[4] == mark and board[2] == mark):
        return True
    else:
        return False

def spotOpen(position):
    if board[position] == '-':
        return True

def openMoves(board):
    for i in range(0,len(board)-1):
        if board[i] == '-':
            print("There are still open moves.")
            return True
        else:
            continue
        print("There are no available moves left, game is over.")
        return False

def renderBoard():
    # Ties in to frontend #
    # flash(board)
    print(board[0], board[1], board[2])
    print(board[3], board[4], board[5])
    print(board[6], board[7], board[8])


def startGame():
    print("Game starting! Board is represented by a grid with positions 0 through 8, starting in the top left, ending in the bottom right, and reading left to right.")
    createBoard()
    renderBoard()

    while (openMoves(board)):

        ## Player Turn ##
        if not (win(board, 'O')):
            print("Player's turn.")
            playerTurn()
            renderBoard()
        else:
        # AI's previous turn resulted in a win #
            print("Game over, AI wins.")
            break
        
        ## AI Turn ##
        if not (win(board, 'X')):
            turn = aiTurn()
            print(f"AI intends on going position {turn}")
            if turn in range (9):
                print("AI attempts to take position")
                makeMove(turn, 'O')
                renderBoard()
            else:
            # If AI has no available moves, the game is tied #
                print("Game ends in a draw.")
                break
        
        else:
            print("Game over, player wins.")
            break
    if openMoves(board) == False:
        print("Game ends, it is a draw.")
        






startGame()