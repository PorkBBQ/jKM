#!/usr/bin/python
import sys

#-- map -----------------------------------------
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
    print(jsonStr)




'''

hadoop fs -rmr /tmp/dsc01_01e

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_01e \
-file /home/biadmin/josh/script/dsc01/dsc01_01e_map.py \
-mapper /home/biadmin/josh/script/dsc01/dsc01_01e_map.py

'''


hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_01e \
-mapper /bin/cat

