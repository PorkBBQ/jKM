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
        if typeStr == 'dict':
            for _4 in _3.keys():
                intermediate.append(_2+':'+typeStr+':'+str(_4))
        if typeStr in ['int', 'float']:
            intermediate.append(_2+':'+typeStr+':'+str(_3))
        else:
            intermediate.append(_2+':'+typeStr+':_total')
        
#-- /map -----------------------------------------
len(jsons)
#len(intermediate)

#-- reduce -----------------------------------------

d = dict()
for line in intermediate:
    row = line.split(":", 3)

    if row[1] in ['dict']:
        if row[0]+':'+row[1 ]+':'+row[2] not in d:
            d[row[0]+':'+row[1]+':'+row[2]]=1
        else:
            d[row[0]+':'+row[1]+':'+row[2]]+=1
    elif row[1] in ['int']:
        if row[0]+':'+row[1]+':count' not in d:
            d[row[0]+':'+row[1]+':count']=1
            d[row[0]+':'+row[1]+':min']=int(row[2])
            d[row[0]+':'+row[1]+':max']=int(row[2])
            d[row[0]+':'+row[1]+':sum']=int(row[2])
        else:
            d[row[0]+':'+row[1]+':count']+=1
            d[row[0]+':'+row[1]+':min']=min(d[row[0]+':'+row[1]+':min'], int(row[2]))
            d[row[0]+':'+row[1]+':max']=max(d[row[0]+':'+row[1]+':max'], int(row[2]))
            d[row[0]+':'+row[1]+':sum']+=int(row[2])
    elif row[1] in ['float']:
        if row[0]+':'+row[1]+':count' not in d:
            d[row[0]+':'+row[1]+':count']=1
            d[row[0]+':'+row[1]+':min']=float(row[2])
            d[row[0]+':'+row[1]+':max']=float(row[2])
            d[row[0]+':'+row[1]+':sum']=float(row[2])
        else:
            d[row[0]+':'+row[1]+':count']+=1
            d[row[0]+':'+row[1]+':min']=min(d[row[0]+':'+row[1]+':min'], float(row[2]))
            d[row[0]+':'+row[1]+':max']=max(d[row[0]+':'+row[1]+':max'], float(row[2]))
            d[row[0]+':'+row[1]+':sum']+=float(row[2])
    else:
        if row[0]+':'+row[1]+':count' not in d:
            d[row[0]+':'+row[1]+':count']=1
        else:
            d[row[0]+':'+row[1]+':count']+=1

d2=dict()
for k, v in sorted(d.items()):
    row = k.split(":", 3)
    if row[0] not in d2: 
        d2[row[0]]=dict()
        d2[row[0]]['type']=row[1]
    d2[row[0]][row[2]]=v

for k1, v1 in d2.items():
    print('\n'+k1 + ' (' + v1['type'] + '):')
    for k2, v2 in v1.items():
        if k2 == 'type':
            pass
        if k2 == 'sum':
            print('  '+'avg' + '=' + str(v1['sum']/v1['count']))
        else:
            print('  '+k2 + '=' + str(v2))

#-- /reduce -----------------------------------------
