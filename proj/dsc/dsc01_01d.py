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


def expand_dict(d, parentName=''):
    for key, value in d.items():       
        out=parentName + str(key)
        outType=str(type(value)).replace("<type '", "").replace("'>", "")
        intermediate.append(out + " (" + outType + ")")
        if type(value) is dict:
            expand_dict(value, key+':')

expand_dict(jsons[0])
for _ in jsons:
    expand_dict(_)

#-- /map -----------------------------------------

#len(intermediate)

#-- reduce -----------------------------------------

for k, v in sorted(collections.Counter(intermediate).items()):
    print(str(v)+'\t'+str(k))

#-- /reduce -----------------------------------------
