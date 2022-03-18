import random
from flask import Flask, render_template, redirect, session, flash, request
app = Flask(__name__)
app.secret_key = 'super secret key 1234'


board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]

## Routes ##
@app.route('/')
def display_index():
    return render_template('index.html', board = board)

@app.route('/start')
def launch_game():
    startGame()
    return render_template('index.html', board = board)

@app.route('/place', methods=["POST"])
def take_turn():
    myMove = request.form['position']
    takeTurns(myMove)
    return render_template('index.html', board = board)

    

## Game ##
def createBoard():    
    for idx in range (len(board)):
        board[idx] = "-"

def startGame():
    print("Game starting! Board is represented by a grid with positions 0 through 8, starting in the top left, ending in the bottom right, and reading left to right.")
    flash("Game starting! Board is represented by a grid with positions 0 through 8, starting in the top left, ending in the bottom right, and reading left to right.")
    createBoard()
    renderBoard()



def playerTurn(position):
    #Validation logic to ensure user input can be processed#
    run = True
    while run:
        turn = position
        try:
            turn = int(turn)
            #Above ensures they provide an actual number#
            if turn > -1 and turn < 9:
                if spotOpen(turn):
                    run = False
                    makeMove(turn, 'X')
                else:
                    print("This spot is already taken")
                    flash("This spot is already taken")

                    break
            else:
                print('Please provide a number between 0 and 8, that is not an occupied space')
                flash('Please provide a number between 0 and 8, that is not an occupied space')

                break
        except:
            print('Please provide a valid number for an open space')
            flash('Please provide a valid number for an open space')

            break


def aiTurn():
    xspots = board.count("X")
    ospots = board.count("O")
    if not ospots == xspots:

        possibleMoves = [x for x, mark in enumerate(board) if mark == '-']
        #Above will number all "spaces" within the board list to ID them down below#
        move = -1
        #Check a copy of the board for possible wins that are one move away, starting with O
        for mark in ['O', 'X']:
            for i in possibleMoves:
                boardState = board[:]
                #Create clone of board.
                boardState[i] = mark
                #Add one more tile to each spot, checking to see if a win occurs.
                if win(boardState, mark):
                    move = i
                    return move
        #Check to see if a corner is available, and if so, move into a random corner#
        cornersAvailable = []
        for i in possibleMoves:
            if i in [0,2,6,8]:
                cornersAvailable.append(i)
        if len(cornersAvailable) > 0:
            if len(cornersAvailable) == 1:
                move = cornersAvailable[0]
                return move
            if cornersAvailable[1] > cornersAvailable[0]:
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
            move = selectRandom(edgesAvailable)
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
        flash("There are no available moves left, game is over.")
        return False

def renderBoard():
    
    print(board[0], board[1], board[2])
    print(board[3], board[4], board[5])
    print(board[6], board[7], board[8])


def takeTurns(position):
    if (openMoves(board)):

        ## Player Turn ##
        if not (win(board, 'O')):
            print("Player's turn.")
            playerTurn(position)
            renderBoard()
        else:
        # AI's previous turn resulted in a win #
            print("Game over, AI wins.")
            # break
        
        ## AI Turn ##
        if not (win(board, 'X')):
            turn = aiTurn()
            print(f"AI intends on going position {turn}")
            if turn in range (9):
                print("AI attempts to take position")
                makeMove(turn, 'O')
                #Check once more for AI win
                if (win(board, 'O')):
                    print("Game over, AI wins.")
                    flash("Game over, AI wins.")

                renderBoard()
            else:
                print("Game ends in a draw.")
                flash("Game ends in a draw.")
        
        else:
            print("Game over, player wins.")
            flash("Game over, player wins.")

    if openMoves(board) == False:
        print("Game ends, it is a draw.")
        flash("Game ends, it is a draw.")
        

if __name__=="__main__":
    app.run(debug=True)