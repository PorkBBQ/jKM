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
    _ = _.strip()
    jsonStr=_.replace('""', '"')
    for _1, _2 in replaceList:
        jsonStr = jsonStr.replace(_1, _2)
    jsons.append(json.loads(jsonStr))
    
for _1 in jsons:
    for _2, _3 in _1.items():
        typeStr=str(type(_3)).replace("<type '", "").replace("'>", "")
        print(_2+':'+typeStr)


'''

hadoop fs -rmr /tmp/dsc01_01b

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_01b \
-file /home/biadmin/josh/script/dsc01/dsc01_01b_map.py \
-mapper /home/biadmin/josh/script/dsc01/dsc01_01b_map.py \
-reducer "uniq -c" \
-combiner "uniq -c"

'''