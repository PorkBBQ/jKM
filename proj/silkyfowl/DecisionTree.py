# -*- coding: utf-8 -*-

import math
def calEntropy(dataSet):
    numEntries = len(dataSet)
    labelCount={}
    for data in dataSet:
        currentLabel = data[-1]
        labelCount[currentLabel] = labelCount.get(currentLabel, 0) + 1
        entropy=0.0
    for key in labelCount:
        prob=float(labelCount[key])/numEntries
        entropy -=prob * math.log(prob,2)
    return entropy

def getData():
    dataSet=[
        [1,1,'y']
        , [1,1,'y']
        , [1,0,'n']
        , [0,1,'n']
        , [0,1,'n']
    ]
    labels = ['no surfacing', 'flippers']
    
    return dataSet, labels

dataSet, labels = getData()

calEntropy(dataSet)

def splitDataSet(dataSet, axis, value):
    retDataSet=[]
    for data in dataSet:
        if data[axis] == value:
            reducedData = data[:axis]
            reducedData.extend(data[axis+1:])
            retDataSet.append(reducedData)
    return retDataSet

splitDataSet(dataSet, 0, 0)

def chooseBestFeatureToSplit():
    numFeatures = len(dataSet[0])-1
    baseEntropy = calEntropy(dataSet)
    bestInfoGain = 0.0
    bestDeature = -1
    for i in range(numFeatures):
        
        
