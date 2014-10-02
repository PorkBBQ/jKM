#!/usr/bin/python

import json
import sys

jsons=[]
replaceList=[]
replaceList.append(['"craetedAt":', '"createdAt":'])
replaceList.append(['"created_at":', '"createdAt":'])
replaceList.append(['"session_id":', '"sessionID":'])
replaceList.append(['"user_agent":', '"userAgent":'])
replaceList.append(['"item_id":', '"itemId":'])

drillColumns={
    'auth':False
    , 'createdAt':False
    , 'payload':True
    , 'refId':False
    , 'sessionID':False
    , 'type':True
    , 'user':False
    , 'userAgent':False
    , 'payload:results':False
    , 'payload:recommended':False
    , 'payload:popular':False
    , 'payload:marker':False
    , 'payload:recent':False
    , 'payload:itemId':False
    , 'payload:length':False
    , 'payload:recs':False
}

def expand_dict(d, parentName='', drillDown =True):
    for k, v in d.items():
        p=parentName+str(k)
        
        if p in drillColumns:
            drillDown=drillColumns[p]
        else:
            drillDown=True
        p+=":"
        
        print(p)
        if type(v) is list:
            if drillDown==True:
                expand_list(v, p, drillDown)
        elif type(v) is dict:
            if drillDown==True:
                expand_dict(v, p, drillDown)
        else:
            if drillDown==True:
                print(p+str(v))
            
def expand_list(l, parentName='', drillDown=True):
    for _ in l:
        p=parentName+'$'
        if type(_) is list:
            if drillDown==True:
                print(p)
        elif type(_) is dict:
            if drillDown==True:
                print(p)
        else:
            if drillDown==True:
                print(p+str(_))

#-- /map -----------------------------------------

for _ in sys.stdin:
    _=_.strip()
    jsonStr=_.replace('""', '"')
    for _1, _2 in replaceList:
        jsonStr = jsonStr.replace(_1, _2)
    expand_dict(json.loads(jsonStr), drillDown=False)



"""

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_01f \
-file /home/biadmin/josh/script/dsc01/dsc01_01f_map.py \
-mapper /home/biadmin/josh/script/dsc01/dsc01_01f_map.py \
-reducer "uniq -c"

"""