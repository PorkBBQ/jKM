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
        if typeStr == 'dict':
            for _4 in _3.keys():
                print(_2+':'+typeStr+':'+str(_4))
        if typeStr in ['int', 'float']:
            print(_2+':'+typeStr+':'+str(_3))
        else:
            print(_2+':'+typeStr+':_total')

'''

hadoop fs -rmr /tmp/dsc01_01c

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_01c \
-file /home/biadmin/josh/script/dsc01/dsc01_01c_map.py \
-mapper /home/biadmin/josh/script/dsc01/dsc01_01c_map.py \
-file /home/biadmin/josh/script/dsc01/dsc01_01c_reduce.py \
-reducer /home/biadmin/josh/script/dsc01/dsc01_01c_reduce.py


-numReduceTasks 10


'''



'''
auth (unicode):	
  count=351712	
  type=unicode	
	
payload (dict):	
  itemId=329525	
  _total=609352	
  subAction=177	
  old=134	
  rating=926	
  popular=5425	
  recommended=5425	
  results=1328	
  item_id=256114	
  length=274	
  recs=1344	
  marker=559731	
  new=134	
  type=dict	
  recent=5425	
	
sessionID (unicode):	
  count=612873	
  type=unicode	
	
user (int):	
  count=612873	
  max=99985450	
  avg=50189405	
  type=int	
  min=1091145	
	
userAgent (unicode):	
  count=612873	
  type=unicode	
	
type (unicode):	
  count=612873	
  type=unicode	
	
refId (unicode):	
  count=351712	 
  type=unicode	
	
createdAt (unicode):	
  count=612873	
  type=unicode	
  
'''