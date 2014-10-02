# -*- coding: utf-8 -*-

def stem(word, method='1'):
    import re
    if method==0:
        return word
    if '1' in method:
        pattern='\w+.*\w+|\w{1}'
        res=re.search(pattern, word)
        if res:
            return res.group()
        else:
            return ''
            
def getTokens(s, proc='lower', stemMethod='1', keywordList=[]):
    tokens=[]
    for w in s.split(' '):
        if proc=='stem':
            import nltk
            w=nltk.PorterStemmer().stem_word(w).lower()
            w=stem(w, stemMethod)
        elif proc=='lower':
            w=w.lower()
            w=stem(w, stemMethod)
        else:
            w=stem(w)
        if keywordList==[]:
            tokens.append(w)
        else:
            if w in keywordList:
                tokens.append(w)
    return tokens

def getWordCount(docs, proc='lower', stemMethod='1', minCount=1, batchSize=1000):
    import time
    time1=time.time()
    wcTotal=dict()
    length=len(docs)
    
    batches=[]
    for i in range(length//batchSize+1):
        batches.append(docs[i*batchSize:min((i+1)*batchSize, length)])
        
    for batch in batches:
        wc=dict()
        for doc in batch:
            tokens=getTokens(doc, proc=proc, stemMethod=stemMethod)
            for w in tokens:
                if w!='':
                    if w in wc.keys():
                        wc[w]+=1
                    else: 
                        wc[w]=1
        for w in wc.keys():
            if w in wcTotal.keys():
                wcTotal[w]+=wc[w]
            else:
                wcTotal[w]=wc[w]
    sortDesc_0=sorted([(-v, k) for (k, v) in wcTotal.items()])
    sortDesc=[(v, -k) for (k, v) in sortDesc_0 if -k>=minCount]
    print('--> wordcount:%d, in %.2f seconds' % (length, time.time()-time1))
    return sortDesc


def tf(dct):
    tf={}
    for k, v in dct.items():
        tf[k]={}
        tokens=getTokens(v)
        length=len(tokens)
        for token in tokens:
            if token in tf[k]:
                tf[k][token]+=1.0/length
            else:
                tf[k][token]=1.0/length
    return tf


def idf(dct):
    from math import log
    df={}
    length=len(dct)
    for k, v in dct.items():
        tokenSet=set(getTokens(v))
        for token in tokenSet:
            if token in df:
                df[token]+=1.0
            else:
                df[token]=1.0
    idf={}
    for k, v in df.items():
        idf[k]=1.0+log(length/v)
    return idf


def tfidf(dct):
    tf1=tf(dct)
    idf1=idf(dct)
    tfidf={}
    for k1, v1 in tf1.items():
        tfidf[k1]={}
        for k2, v2 in v1.items():
            tfidf[k1][k2]=tf1[k1][k2]*idf1[k2]
    return tfidf            


def cosSim(t1, t2): # given 2 TF-IDF lists
    import nltk
    keys=list(set(t1.keys()+t2.keys()))
    v1=[]
    v2=[]
    for k in keys:
        if k in t1:
            v1.append(t1[k])
        else:
            v1.append(0)
        if k in t2:
            v2.append(t2[k])
        else:
            v2.append(0)        
    
    return nltk.cluster.util.cosine_distance(v1, v2)


def cosSimMatrix(dct):
    csm={}    
    for k1, v1 in dct.items():
        for k2, v2 in dct.items():
            csm[(k1, k2)]=cosSim(v1, v2)
    return csm


def getHieChart(dct):
    import proj.lib.textAnalysis as ta
    import scipy
    import pylab
    import scipy.cluster.hierarchy as sch
    
    #dct={}
    #for item in lst:
    #    dct[item[0]]=item[1]
    lst=dct.items()
    
    tfidf=ta.tfidf(dct)
    mtx=ta.cosSimMatrix(tfidf)
    mtxItems=mtx.items()
    mtxItems.sort()
    
    idKeys=[]
    for _ in lst:
        idKeys.append(_[0])
    idKeys.sort()

    length=len(idKeys)
    D = scipy.zeros([length,length])
    for i in range(length):
        for j in range(length):
            D[i,j] = mtx[(idKeys[i], idKeys[j])]

    fig = pylab.figure(figsize=(12,8))
    ax1 = fig.add_axes()
    Y = sch.linkage(D, method='single')
    dg = sch.dendrogram(Y, leaf_font_size=10)
    
    ids=[]
    for _ in dg['leaves']:
        ids.append([_, idKeys[_]])
        
    return pylab, ids


def apriori(dataset, minSupport=0.1, minConfidence=0.3, keywordList=[]):
    import proj.lib.apriori as apriori

    L, support_data=apriori.apriori(dataset=dataset, minsupport=minSupport)
    r=apriori.generateRules(L=L, support_data=support_data, min_confidence=minConfidence)
    
    temp1=[[list(_[0]), list(_[1]), _[2]] for _ in r]
    temp2=[[v, k1, k2] for k1, k2, v in temp1]
    temp2.sort(reverse=True)
    temp3=[[k1, k2, v] for [v, k1, k2] in temp2]
        
    return temp3
    
