import random
# In the game of Master-Mind, you try to guess a 4-digit code with each digit in the range of 0-5. 
# Each time you guess a number, you're told how close your guess was. 
# For each digit in the code:
#   If that digit appears in your guess in the correct spot, you get 10 points.
#   If that digit appears in your guess in the incorrect spot, you get 1 point.
# For example, if the code is 4444 and your guess is 1234, you would get 13 points
#   The first three 4's appear in your guess but in the wrong spot (1 point each)
#   The last 4 appears in your guess in the correct spot (10 points)
# Write a Python program to play MasterMind.

#===============================================================================

# 1. Write a subroutine which returns a 4-digit number (your code)
def get_code():
    code = []
    for _ in range(4):
        code.append(random.randint(0,5))
    return code

print(get_code())



# 2. Write a subroutine which:
#   Is passed two numbers (your guess and the code), and
#   Returns your score
# 10-points for each digit in the code that's in the correct spot, 1 point for each digit in the code that's in the wrong spot

def get_score(code, guess):
    score = 0
    for i in range(4):
        if code[i] == guess[i]:
            score += 10
        elif code[i] in guess:
            score += 1
    return score

print(get_score([1,2,3,4], [4,3,2,1])) # 4 points



# 3. Write a program which:
#   Starts by generating a code (problem #1)
#   Then prompts you for a guess (0000 to 5555)
#   Scores your guess and tells you your score,
#   Keeps playing until your score is 40 (correct code), and
#   Keeps track of how many guesses it took you

def mastermind():
    code = get_code()
    guesses = 0
    while True:
        guess = input("Enter your guess: ")
        guess = [int(x) for x in guess]
        score = get_score(code, guess)
        guesses += 1
        print("Score: ", score)
        if score == 40:
            print("You guessed the code in", guesses, "guesses!")
            break

mastermind()