# -*- coding: utf-8 -*-

import json
import collections

datafile = open(r'D:\Josh\data\DSC01\heckle\web.log.2')
intermediate=[]
#-- map -----------------------------------------
jsons=[]
replaceList=[]
replaceList.append(['"craetedAt":', '"createdAt":'])
replaceList.append(['"created_at":', '"createdAt":'])
replaceList.append(['"session_id":', '"sessionID":'])
replaceList.append(['"user_agent":', '"userAgent":'])
replaceList.append(['"item_id":', '"itemId":'])

for _ in datafile.readlines():
    print(_)
    jsonStr=_.replace('""', '"')
    for _1, _2 in replaceList:
        jsonStr = jsonStr.replace(_1, _2)
    jsons.append(json.loads(jsonStr))


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
        
        intermediate.append(p)
        if type(v) is list:
            if drillDown==True:
                expand_list(v, p, drillDown)
        elif type(v) is dict:
            if drillDown==True:
                expand_dict(v, p, drillDown)
        else:
            if drillDown==True:
                intermediate.append(p+str(v))
            
def expand_list(l, parentName='', drillDown=True):
    for _ in l:
        p=parentName+'$'
        if type(_) is list:
            if drillDown==True:
                intermediate.append(p)
        elif type(_) is dict:
            if drillDown==True:
                intermediate.append(p)
        else:
            if drillDown==True:
                intermediate.append(p+str(_))

#-- /map -----------------------------------------


for _ in jsons:
    expand_dict(_, drillDown=False)
#len(intermediate)

#-- reduce -----------------------------------------

for k, v in sorted(collections.Counter(intermediate).items()):
    print(str(v)+'\t'+str(k))

#-- /reduce -----------------------------------------


"""
a=[1,2,[31,32,33], {'4':{'41':'41v', '42':[421,422]}}]
d={'a':'a1', 'b':'b1'}

def expand_list(l, parentName=''):
    for _ in l:
        if type(_) is list:
            expand_list(_, parentName+'$')
        elif type(_) is dict:
            expand_dict(_, parentName+'$')
        else:
            print(parentName+str(_))
        

def expand_dict(d, parentName=''):
    for k, v in d.items():
        p=parentName+str(k)+":"
        if type(v) is list:
            expand_list(v, p+'$')
        elif type(v) is dict:
            expand_dict(v, p+'$')
        else:
            print(p+str(v))
            

'''
        out=parentName + str(key)
        outType=str(type(value)).replace("<type '", "").replace("'>", "")
        intermediate.append(out + " (" + outType + ")")
        if type(value) is dict:
            expand_dict(value, key+'::')
'''
        
expand_list(a)

expand_dict(d)
"""