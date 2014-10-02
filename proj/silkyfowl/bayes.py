
import numpy as np

import math

def getDataSet():
    texts = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please']
              , ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid']
              , ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'hime']
              , ['stop', 'posting', 'stupid', 'worthless', 'garbage']
              , ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him']
              , ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    textGroup = [0,1,0,1,0,1]
    return texts, textGroup

def getWordSet(texts):
    wordSet = set([])
    for text in texts:
        wordSet = wordSet | set(text)
    return list(wordSet)
    
def getAppearenceVector(wordSet, text):
    appearenceVector = [0]*len(wordSet)
    for word in text:
        if word in wordSet:
            appearenceVector[wordSet.index(word)]=1
        else:
            print("the word %s is not in my vocabulary!" %word)
    return appearenceVector

def getTrainedBayes(matrix, groups):
    numTexts = len(matrix)
    numWords = len(matrix[0])
    pAbuse = sum(groups)/float(numTexts)
    nums = [np.zeros(numWords), np.zeros(numWords)]
    dens = [0.0, 0.0]
    for i in range(numTexts):
        g = groups[i]
        nums[g] += matrix[i]
        dens[g] += sum(matrix[i])
    return nums[0]/dens[0], nums[1]/dens[1], pAbuse

def classify(vec, p0Vec, p1Vec, pClass1):
    p0 = sum(vec * p0Vec) + math.log(pClass1)
    p1 = sum(vec * p1Vec) + math.log(1.0-pClass1)
    if p1>p0:
        return 1
    else:
        return 0




