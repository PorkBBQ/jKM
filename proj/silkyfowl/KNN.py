# -*- coding: utf-8 -*-

import numpy as np
import collections as col

def getClassification(inX, group, labels, k, normal=True):
    if normal==True:
        inX, group=normalize(inX, group)
    
    tile=np.tile(inX, (group.shape[0], 1))
    diff=group-tile
    diff_sq=diff**2
    dist_sq=diff_sq.sum(axis=1)
    dist=dist_sq**0.5
    arg_order=dist.argsort()
    
    label_cnt={}
    for i in range(k):
        label=labels[arg_order[i]]
        label_cnt[label]=label_cnt.get(label, 0)+1
        
    sorted_label_cnt=sorted([(-v, k) for (k, v) in label_cnt.iteritems()])
    return sorted_label_cnt[0][1]
    
def normalize(inX, group):
    mean=group.mean(axis=0)
    std=group.std(axis=0)
    return (inX-mean)/std, (group-mean)/std
