#!/usr/bin/python

import json
import sys

jsons=[]
replaceList=[]
replaceList.append(['craetedAt', 'createdAt'])
replaceList.append(['created_at', 'createdAt'])
replaceList.append(['session_id', 'sessionID'])
replaceList.append(['user_agent', 'userAgent'])

for _ in sys.stdin:
    _ = _ .strip()
    jsonStr=_.replace('""', '"')
    for _1, _2 in replaceList:
        jsonStr = jsonStr.replace(_1, _2)
    jsons.append(json.loads(jsonStr))


def expand_dict(d, parentName=''):
    for key, value in d.items():       
        out=parentName + str(key)
        outType=str(type(value)).replace("<type '", "").replace("'>", "")
        print(out + " (" + outType + ")")
        if type(value) is dict:
            expand_dict(value, key+':')

for _ in jsons:
    expand_dict(jsons[0])


'''

hadoop fs -rmr /tmp/dsc01_01d

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_01d \
-file /home/biadmin/josh/script/dsc01/dsc01_01d_map.py \
-mapper /home/biadmin/josh/script/dsc01/dsc01_01d_map.py \
-reducer "uniq -c"


'''
