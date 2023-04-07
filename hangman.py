import requests
from os import system, name
from time import sleep
import random
from datetime import datetime

apiUrl = "http://127.0.0.1:5000/api/scores"
apiSecret = "verySecretPassword123321"

with open("words.txt") as wordsFile:
    words = wordsFile.read().splitlines()

header = f"""
------------------
-  Hangman Game  -
------------------


"""


def main():
    while True:
        clear()
        print(header)
        print("1. Play Game")
        print("2. Display High Scores")
        try:
            choice = int(input("\nChoice: "))
        except BaseException:
            choice = 0
        if choice == 1:
            playGame()
        elif choice == 2:
            print("\n\x1B[4mHIGH SCORES - TOP 50\x1B[0m\n")
            data = requests.get(apiUrl, params={"limit": 50, "sort": "asc"}, headers={"Authorization": apiSecret})
            for item in data.json():
                print(f"{secondsConverter(item['score'])}, {item['name']}")
            input("\nPress Enter to continue...")
        else:
            print("Not valid number...")
            sleep(1)


def secondsConverter(seconds):
    min, sec = divmod(seconds, 60)
    if min:
        return f"{min} min {sec} sec"
    else:
        return f"{sec} sec"


def playGame():
    triesLeft = 6
    guessedLetters = []
    correctLetters = []
    randomWords = random.sample(words, 3)
    for i in range(3):
        clear()
        print(header)
        print(f"Game starting in {3-i}")
        sleep(1)
    currentWordIndex = 0
    startTime = datetime.now()

    while True:
        clear()
        revealedWord = ""
        for letter in randomWords[currentWordIndex]:
            if letter in correctLetters:
                revealedWord += f" {letter} "
            else:
                revealedWord += " _ "
        if revealedWord.replace(" ", "") == randomWords[currentWordIndex]:
            if currentWordIndex == 2:
                gameWin((datetime.now() - startTime).seconds)
                break
            else:
                currentWordIndex += 1
                triesLeft = 6
                guessedLetters.clear()
                correctLetters.clear()
                continue

        print(
            f"Word {currentWordIndex + 1}/3\nElapsed time (updates every refresh): {(datetime.now() - startTime).seconds} seconds\nGuessed letters: {' '.join(guessedLetters)}")
        print(hangmanPics[6 - triesLeft] + "\n")
        print(f"{revealedWord}\n")
        letter = input("Guess the letter: ").lower()
        if len(letter) == 1:
            if letter.isalpha() == False:
                print("Numbers not allowed")
                sleep(1)
            elif letter not in guessedLetters:
                guessedLetters.append(letter)
                if letter in randomWords[currentWordIndex]:
                    correctLetters.append(letter)
                else:
                    triesLeft -= 1
            else:
                print("Letter already guessed")
                sleep(1)
        else:
            print("Input only 1 letter.")
            sleep(1)
        if triesLeft <= 0:
            gameOver(randomWords[currentWordIndex])
            break


def gameWin(elapsedSeconds):
    while True:
        clear()
        print(f"You win! It took {elapsedSeconds} seconds.\n")
        print("Saving High Score to Cloud.\n")
        name = input("Your name: ")
        if len(name) > 0:
            requests.post(apiUrl, json={"name": name, "score": elapsedSeconds}, headers={"Authorization": apiSecret})
            break
        else:
            print("You did not enter a name...")
            sleep(1)


def gameOver(word):
    while True:
        clear()
        print(hangmanPics[6] + "\n")
        print(f"Word was: {word}\n")
        print("You lost. Try again?\n\nY: Yes!\nN: No!\n")
        choice = input("Choice: ")
        if choice.upper() == "Y":
            playGame()
            break
        elif choice.upper() == "N":
            break
        else:
            print("Not valid letter...")
            sleep(1)


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


hangmanPics = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========''']

if __name__ == '__main__':
    main()
