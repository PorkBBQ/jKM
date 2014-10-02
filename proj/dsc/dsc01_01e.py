# -*- coding: utf-8 -*-

datafile = open(r'D:\Josh\data\DSC01\heckle\web.log.2')
intermediate=[]

#-- map -----------------------------------------
jsons=[]
replaceList=[]
replaceList.append(['craetedAt', 'createdAt'])
replaceList.append(['created_at', 'createdAt'])
replaceList.append(['session_id', 'sessionID'])
replaceList.append(['user_agent', 'userAgent'])

i=0
for _ in datafile.readlines():
    _ = _.strip()
    i+=1
    jsonStr=_.replace('""', '"')
    for _1, _2 in replaceList:
        jsonStr = jsonStr.replace(_1, _2)
    intermediate.append(jsonStr)


print(len(intermediate))
print(i)