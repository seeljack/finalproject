import random
from flask import Flask, render_template
import flask
import random
import subprocess
import time
app = Flask(__name__)
# List of possible words

mylist = ["booby", "boobs"];


# Helper Functions

# Picks the correct word
def correct_answer():
    x = random.randint(0,1)
    return mylist[x]

# Gets the user input
def user_input(correct):
    wrong = False
    guess = input("Guess a word \n")
    guess_low = guess.lower()
    if len(guess) == 5:
        for letter in range(5):
            if correct[letter] == guess_low[letter]:
                print(guess[letter] + " ", end = '')
            else:
                print("X ", end = '')
                wrong = True
        if wrong == True:
            return False
        else:
            return True
    else:
        print("Must be 5 letters")
        return False







# Driver

@app.route('/wordle')
def wordle():
    return '<h1>Hello</h1>'
    # print("Welcome to Booble \nFind the right word \nX X X X X")
    # correct = correct_answer()
    # while user_input(correct) == False:
    #     print("\nTry again \N{smiling face with smiling eyes}\n")
    # print("Congrats you won!\N{Party Popper} ")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
