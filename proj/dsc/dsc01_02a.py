#!/home/biadmin/anaconda/bin/python

import json
import sys
import collections

def getReplaceList():
    replaceList=[]
    replaceList.append(['""', '"'])
    replaceList.append(['"craetedAt":', '"createdAt":'])
    replaceList.append(['"created_at":', '"createdAt":'])
    replaceList.append(['"session_id":', '"sessionID":'])
    replaceList.append(['"user_agent":', '"userAgent":'])
    replaceList.append(['"item_id":', '"itemId":'])
    return replaceList

def mapOut(item):
    for _ in item.keys():
        out=_
        if env=='local':
            intermediate.append(out)
        elif env=='mr':
            print(out)

def mapper(env):
    if env=='local':
        datafile = open(localFile)
        it=datafile.readlines()
    elif env=='mr':
        it=sys.stdin
    for _ in it:
        _ = _.strip()
        for r1, r2 in getReplaceList():
            _ = _.replace(r1, r2)
        mapOut(json.loads(_))


def reducer(env='local'):    
    if env=='local':
        it=intermediate 
    elif env=='mr':
        it=sys.stdin
        
    freq=sorted(collections.Counter(it).items())
    for _1, _2 in freq:
        print('%d\t%s' % (_2, _1.strip()))

env='local' if len(sys.argv)==1 else 'mr'

localFile=r'D:\Josh\data\DSC01\heckle\web.log.2'
if env=='local':
    intermediate=[]
    mapper('local')
    reducer('local')
elif env=='mr':
    if sys.argv[1]=='-m':
        mapper('mr')
    elif sys.argv[1]=='-r':
        reducer('mr')

'''

hadoop fs -rmr /tmp/dsc01_02a

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_01a' \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_02a \
-file /home/biadmin/josh/script/dsc01/dsc01_02a.py \
-mapper "/home/biadmin/josh/script/dsc01/dsc01_02a.py -m" \
-reducer "/home/biadmin/josh/script/dsc01/dsc01_02a.py -r"

'''
