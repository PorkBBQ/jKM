#!/usr/bin/python

import json
import sys

#-- map -----------------------------------------
jsons=[]
replaceList=[]
replaceList.append(['"craetedAt":', '"createdAt":'])
replaceList.append(['"created_at":', '"createdAt":'])
replaceList.append(['"session_id":', '"sessionID":'])
replaceList.append(['"user_agent":', '"userAgent":'])
replaceList.append(['"item_id":', '"itemId":'])

drillPaths={
    'auth':0
    , 'createdAt':0
    , 'payload':1
    , 'refId':0
    , 'sessionID':0
    , 'type':1
    , 'user':0
    , 'userAgent':0
    , 'payload:results':0
    , 'payload:recommended':0
    , 'payload:popular':0
    , 'payload:marker':0
    , 'payload:recent':0
    , 'payload:itemId':0
    , 'payload:length':0
    , 'payload:recs':0
}

drillPathType={
    'auth':'1'
    , 'createdAt':'1'
    , 'payload':'1'
    , 'refId':'1'
    , 'sessionID':'1'
    , 'type':'1'
    , 'user':'num'
    , 'userAgent':'1'
    , 'payload:results':'1'
    , 'payload:recommended':'1'
    , 'payload:popular':'1'
    , 'payload:marker':'1'
    , 'payload:recent':'1'
    , 'payload:itemId':'1'
    , 'payload:length':'1'
    , 'payload:recs':'1'
}

def expand(item, path='', isDrill=True):
    if type(item) is list:
        for _ in dict():
            p=path+'$'+str(_)
            mapOut(p, str(_))
            if p in drillPaths:
                isDrill=drillPaths[p]
            if isDrill:
                expand(_, p, isDrill)
    elif type(item) is dict:
        for k, v in item.items():
            p=path+str(k)
            mapOut(p, str(v))
            if p in drillPaths:
                isDrill=drillPaths[p]
            if isDrill:
                p+=':'
                expand(v, p, isDrill)
    else:
        p=path+str(item)
        mapOut(p, str(item))

def mapOut(k, v='', t='3'):
    #print(k)    
    #intermediate.append(k)
    if k in drillPathType:
        t=drillPathType[k]
    print(k + '\t' + str(v) + '\t' + str(t))

for _ in sys.stdin:
    _=_.strip()
    jsonStr=_.replace('""', '"')
    for _1, _2 in replaceList:
        jsonStr = jsonStr.replace(_1, _2)
    jsons.append(json.loads(jsonStr))
    expand(json.loads(jsonStr), '')

#-- /map -----------------------------------------




'''
hadoop fs -rmr /tmp/dsc01_01g

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_01g \
-file /home/biadmin/josh/script/dsc01/dsc01_01g_map.py \
-mapper /home/biadmin/josh/script/dsc01/dsc01_01g_map.py \
-file /home/biadmin/josh/script/dsc01/dsc01_01g_reduce.py \
-reducer /home/biadmin/josh/script/dsc01/dsc01_01g_reduce.py

'''