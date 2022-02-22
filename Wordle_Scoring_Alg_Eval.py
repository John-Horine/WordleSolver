import Wordle_Solver as ws
from Wordle_Solver import totalAllowedGuesses
from Wordle import Wordle, totalWordList
import collections

def evalScoringAlg1():
    scoringList=[]
    for word in totalWordList:
        currentWordList=totalWordList
        guess="raise"
        wordleBot = Wordle(word)
        isOver= False
        while not isOver:
            if(guess==word):
                isOver=True
                scoringList.append(wordleBot.guessNumber+1)
            elif(wordleBot.guessNumber>=wordleBot.maxGuess):
                isOver=True
                print(word)
                scoringList.append(7)
            else:
                pattern = wordleBot.takeTurn(guess)
                currentWordList = ws.reduceList(guess,pattern,currentWordList)
                guess= ws.chooseWord(currentWordList)
    print(collections.OrderedDict(sorted(collections.Counter(scoringList).items())))
    averageDict= collections.OrderedDict(sorted(collections.Counter(scoringList).items()))
    score=0
    for key in averageDict:
        score += averageDict[key]/len(totalWordList) * (key +1)
    print(score)

def evalScoringAlg2():
    scoringList=[] # initializes empty list to keep track of guess Numbers
    for word in totalWordList: #iterates through every possible target word 
        wordleBot = Wordle(word)
        scoringAlg2FirstStep(wordleBot)
        isOver= False #initializes boolean variable isOver to false
        while not isOver:
            if(guess==word or wordleBot.guessNumber>=wordleBot.maxGuess):
                isOver=True
                scoringList.append(wordleBot.guessNumber+1) #ends current iteration of loop and adds guess number to scoringList
            else:
                pattern = wordleBot.takeTurn(guess) #increment guessNumber and returns pattern based on most recent guess
                currentWordList = ws.reduceList(guess,pattern,currentWordList) #reduces list based on most recent guess, pattern, and wordlist
                guess= ws.chooseWord(currentWordList) #creates new best guess based on reduced list
    print(collections.OrderedDict(sorted(collections.Counter(scoringList).items()))) #prints sorted list of tuples
    averageDict= collections.OrderedDict(sorted(collections.Counter(scoringList).items()))
    score=0 # initializes scoring algorithm score variable to 0 
    for key in averageDict:
        score += averageDict[key]/len(totalWordList) * (key +1)
    print(score)

def scoringAlg2FirstStep(wordleBot):
    currentWordList=totalAllowedGuesses #sets currentwordlist to total allowed guesses list
    guess="roate" #initializes guess to the optimal word for this scoring algorithm to save time 
    pattern = wordleBot.takeTurn(guess) #increment guess and return pattern
    currentWordList = ws.reduceList(guess,pattern,currentWordList) # sets current word list to reduced list based on guess and pattern   
    guess= ws.chooseWord2(currentWordList) #sets guess using the chooseWord2 scoring algorithm 
    currentWordList = [word for word in totalWordList if word in currentWordList] #sets currentword list to the intersection of the reduced currentwordlist (contains impossible final answers) and totalwordlist

evalScoringAlg2()


            



    

