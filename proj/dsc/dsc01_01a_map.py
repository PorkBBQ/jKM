#!/usr/bin/python

import json
import sys

jsons=[]
for _ in sys.stdin:
    _ = _.strip()
    jsonStr=_.replace('""', '"')
    jsons.append(json.loads(jsonStr))
    
for _1 in jsons:
    for _2 in _1.keys():
        print(_2)
        
        
'''

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_01a \
-file /home/biadmin/josh/script/dsc01/dsc01_01a_map.py \
-mapper /home/biadmin/josh/script/dsc01/dsc01_01a_map.py \
-reducer "uniq -c"

'''