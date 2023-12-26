import random

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

print("Welcome to Booble \nFind the right word \nX X X X X")
correct = correct_answer()
while user_input(correct) == False:
    print("\nTry again \N{smiling face with smiling eyes}\n")
print("Congrats you won!\N{Party Popper} ")


def main():


	if __name__ == "__main__":
		main()
