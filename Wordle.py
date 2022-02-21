import random as rd
totalWordList= open("words.csv").read().splitlines()
WIN_PATTERN=[2,2,2,2,2]

class Wordle:
    def __init__(self, word, maxGuess=6):
        self.word = word
        self.guessNumber=0
        self.maxGuess = maxGuess

    def gameLoop(self):
        isOver = False
        while not isOver:
            self.guessNumber +=1
            guess = input("Input guess: ")
            pattern = self.generatePattern(guess)
            if(pattern==WIN_PATTERN):
                isOver=True
                print("you win")
            elif(self.guessNumber==self.maxGuess):
                isOver=True
                print("youre air")

    def takeTurn(self,guess):
        self.guessNumber +=1
        pattern = self.generatePattern(guess)
        return pattern

    
    def generatePattern(self,guess):
        patternList = []
        for index, letter in enumerate(guess):
            if(self.word[index]==letter):
                patternList.append(2)
            elif(self.word[index]!=letter and letter in self.word):
                patternList.append(1)
            else:
                patternList.append(0)
        return patternList


