# -*- coding: utf-8 -*-
"""
Created on Wed Dec 04 13:47:48 2013

@author: 1309075
"""

class KMeans:
    
    def __init__(self, data, k):
        from scipy.cluster.vq import kmeans2
        import numpy as np
        self.data=data
        self.k=k
        self.centroids, self.groups=kmeans2(np.array(data), k)
        
    def getCentroids(self):
        return self.centroids

    def getGroups(self):
        return self.groups
        
    def getStdevs(self):
        centroids=self.getCentroids()
        groups=self.getGroups()
        
        cals=list()
        for i in range(len(self.data)):
            cals.append([self.data[i], groups[i], centroids[groups[i]]])
        
        for p in cals:
            p.append((p[0][0]-p[2][0])**2+(p[0][1]-p[2][1])**2)
        
        diff_sqs=dict()
        cnts=dict()
        for i in range(self.k):
            diff_sqs[i]=0
            cnts[i]=0
            for p in cals:
                if p[1]==i:
                    diff_sqs[i]+=p[3]
                    cnts[i]+=1
        
        stdevs=list()
        for i in range(self.k):
            try:
                stdevs.append(abs(diff_sqs[i])**0.5/(cnts[i]-1))
            except Exception:
                return 1
            
        #diff_sqs
        #cnts
        return stdevs
