from flask import Flask, render_template, redirect, session, flash
app = Flask(__name__)
app.secret_key = 'super secret key 1234'
from tictactoe import startGame, takeTurns

@app.route('/')
def display_index():
    return render_template('index.html')

@app.route('/start')
def launch_game():
    startGame()

@app.route('/place')
def take_turn(board,position):
    takeTurns(board,position)


if __name__=="__main__":
    app.run(debug=True)