from tkinter import scrolledtext
from numpy import average
import Wordle_Solver as ws
from Wordle import Wordle, totalWordList
import collections



def evalScoringAlg():
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

evalScoringAlg()


            



    

