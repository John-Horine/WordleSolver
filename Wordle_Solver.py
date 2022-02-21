currentWordList= open("words.csv").read().splitlines()
totalWordList= open("words.csv").read().splitlines()

def reduceList(word,infoList,currentWordList):
    for index, letter in enumerate(word):
        if(infoList[index]==0):
            currentWordList= list(filter(lambda x: not(letter in x),currentWordList))
        elif(infoList[index]==1):
            currentWordList= list(filter(lambda x: letter in x and x[index] != letter,currentWordList))
        elif(infoList[index]==2):
            currentWordList= list(filter(lambda x: x[index] == letter,currentWordList))
    return currentWordList

def convert_To_Len_th_base(n, arr, Len, L):
    myList=[]
    for j in range(L):
        myList.append(arr[n % Len])
        n //= Len
        if ((j+1)%5==0):
            return myList


def printf(arr, Len, L):
    totalList=[]
    for i in range(pow(Len, L)):
        totalList.append(convert_To_Len_th_base(i, arr, Len, L))
    return totalList

def evaluateWord(word,currentWordList):
    score=0
    currentWordListCopy=currentWordList
    for pattern in printf([0,1,2],3,5):
        reducedList= reduceList(word,pattern,currentWordList)
        score+= (len(reducedList)/len(currentWordList))*len(reducedList)
        currentWordList=currentWordListCopy
    return score

def chooseWord(currentWordList):
    minvalue= 10000000
    minword = ""
    for element in currentWordList:
        wordEval= evaluateWord(element,currentWordList)
        if wordEval < minvalue:
            minword=element
            minvalue =wordEval
    return minword

def play():
    wordlist=currentWordList
    bestGuess = "raise"
    print("the best Guess is " + bestGuess)
    for i in range(6):
        pattern= input("Insert Pattern with no spaces, 0 is gray, 1 is yellow, 2 is green")
        splitPattern = [int(num) for num in pattern]
        wordlist = reduceList(bestGuess,splitPattern,wordlist)
        print(wordlist)
        bestGuess = chooseWord(wordlist)
        print("the best Guess is " + bestGuess)
