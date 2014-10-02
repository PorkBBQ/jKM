# -*- coding: utf-8 -*-

import json
import collections

datafile = open(r'D:\Josh\data\DSC01\heckle\web.log.2')
intermediate=[]
#-- map -----------------------------------------
jsons=[]
replaceList=[]
replaceList.append(['craetedAt', 'createdAt'])
replaceList.append(['created_at', 'createdAt'])
replaceList.append(['session_id', 'sessionID'])
replaceList.append(['user_agent', 'userAgent'])

for _ in datafile.readlines():
    jsonStr=_.replace('""', '"')
    for _1, _2 in replaceList:
        jsonStr = jsonStr.replace(_1, _2)
    jsons.append(json.loads(jsonStr))

for _1 in jsons:
    for _2, _3 in _1.items():
        typeStr=str(type(_3)).replace("<type '", "").replace("'>", "")
        #print(_2+':'+typeStr)
        intermediate.append(_2+':'+typeStr)
        
#-- /map -----------------------------------------


#-- reduce -----------------------------------------

counter=collections.Counter(intermediate)
for _ in counter.items():
    print(_)
        
#-- /reduce -----------------------------------------
