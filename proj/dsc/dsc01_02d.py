#!/home/biadmin/anaconda/bin/python

import json
import sys
import collections
import dateutil.parser as dp

digits=[str(_) for _ in range(1,101)]

def getReplaceList():
    replaceList=[]
    replaceList.append(['""', '"'])
    replaceList.append(['"craetedAt":', '"createdAt":'])
    replaceList.append(['"created_at":', '"createdAt":'])
    replaceList.append(['"session_id":', '"sessionID":'])
    replaceList.append(['"user_agent":', '"userAgent":'])
    replaceList.append(['"item_id":', '"itemId":'])
    return replaceList

def getDrillPaths():
    return {
        '/auth':0
        , '/createdAt':0
        , '/payload':1
        , '/refId':0
        , '/sessionID':0
        , '/type':1
        , '/user':0
        , '/userAgent':0
        , '/payload/itemId':0
        , '/payload/marker':0
        , '/payload/popular':1
        , '/payload/recent':0
        , '/payload/recommended':1
        , '/payload/recs/':1
        , '/payload/results':1
    }

def getSummaryTypes():    
    return {
        '/auth':'3'
        , '/createdAt':'date'
        , '/payload':'1'
        , '/refId':'3'
        , '/sessionID':'3'
        , '/type':'3'
        , '/user':'num'
        , '/userAgent':'1'
        , '/payload/itemId':'num'
        , '/payload/lengtg':'num'
        , '/payload/marker':'num'
        , '/payload/new':'freq10'
        , '/payload/old':'freq10'
        , '/payload/popular':'1'
        , '/payload/popular/':'freq10'
        , '/payload/rating':'freq10'
        , '/payload/recent':'3'
        , '/payload/recs':'3'
        , '/payload/recs/':'freq10'
        , '/payload/recommended':'3'
        , '/payload/recommended/':'freq10'
        , '/payload/results':'1'
        , '/payload/results/':'freq10'
    }   

def expand(item, path='', group='/'):
    drillPaths=getDrillPaths()
    if type(item) is dict:
        for k, v in item.items():
            p=path + '/' + str(k)
            t='dict'
            mapOut(p, str(v), t, g=group)
            d=drillPaths[p] if p in drillPaths else False
            if d: 
                expand(v, p, group=group)
                
    elif type(item) is list:
        for _ in item:
            p=path+'/'
            t='list'
            mapOut(p, str(_), t, g=group)
            d=drillPaths[p] if p in drillPaths else False
            if d: 
                expand(v, p, group=group)
    else:
        p=path+'/'+str(item)
        t=str(type(item)).replace("<type '", "").replace("'>", "")
        mapOut(p, str(item), t, g=group)


def mapOut(k, v='', t='', s='', g='/'):
    pathTypes=getSummaryTypes()
    if t in ['dict', 'list']:
        s='3'
    if k in pathTypes:
        s=pathTypes[k]
    out=k + '\t' + str(v) + '\t' + t + '\t' + str(s) + '\t' + g
    if env=='local':
        intermediate.append(out)
    elif env=='mr':
        print(out)

def mapper(env):

    it=open(inputFile).readlines() if env=='local' else sys.stdin

    for _ in it:
        _ = _.strip()
        for r1, r2 in getReplaceList():
            _ = _.replace(r1, r2)
        j=json.loads(_)
        if 'createdAt' in j:
            createdAt=dp.parse(j['createdAt']).strftime('%Y/%m/%d')
            try:
                createdAt=dp.parse(j['createdAt']).strftime('%Y/%m/%d')
            except ValueError:
                createdAt='_err: '
                
            if env=='local':
                intermediate.append(createdAt)
            elif env=='mr':
                print(createdAt)
                
def reducer(env='local'):
    it=intermediate if env=='local' else sys.stdin
    for k, v in collections.Counter(it).iteritems():
        print('%d\t%s' %(v, k))


env='local' if len(sys.argv)==1 else 'mr'

if env=='local':
    inputFile=r'D:\Josh\data\DSC01\heckle\web.log.2'
    intermediate=[]
    mapper('local')
    reducer('local')
elif env=='mr':
    if sys.argv[1]=='-m':
        mapper('mr')
    elif sys.argv[1]=='-r':
        reducer('mr')


    
'''

hadoop fs -rmr /tmp/dsc01_02d

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_01d' \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_02d \
-file /home/biadmin/josh/script/dsc01/dsc01_02d.py \
-mapper "/home/biadmin/josh/script/dsc01/dsc01_02d.py -m" \
-reducer "uniq -c"

-reducer "/home/biadmin/josh/script/dsc01/dsc01_02d.py -r"

'''

'''
a='2013-05-06T08:00:08Z'
b='2013-05-12T23:06:11-08:00'

import dateutil

dateutil.parser.parse(a).strftime('%Y/%m/%d')
dateutil.parser.parse(b).strftime('%Y/%m/%d')
'''
