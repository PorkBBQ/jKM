# -*- coding: utf-8 -*-

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from collections import Counter
def getDataSet():
    group=np.array([[1.0,1.1], [1.0,1.0], [0,0], [0,0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels
    
group, labels = getDataSet()
inX = [0,0.1]

def getEuclideanDistance(a, b):
    diff = a-b
    sqrt = diff**2
    sqrt_sum = sqrt.sum()
    distance = sqrt_sum**0.5
    return distance

def getManhattanDistance(a, b):
    diff = a-b
    diff_abs = abs(diff)
    distance = sum(diff_abs)
    return distance

def getKDistances(inX, dataSet, labels, k, distanceCalc):
    distances = [distanceCalc(np.array(vec), np.array(inX)) for vec in dataSet]
    labeled_distances = zip(labels, distances)
    return sorted(labeled_distances, key=lambda p : p[1])[:k]

kDistances = getKDistances(inX, group, labels, 3, getEuclideanDistance)
#kDistances = getKDistances(inX, group, labels, 3, getManhattanDistance)
kDistances

counter=Counter([_[0] for _ in kDistances])
classification = sorted(counter.items(),  reverse=True, key=lambda p : p[1])[0]
classification 

plt.scatter(group[:,0], group[:,1], 'r')
plt.show()
