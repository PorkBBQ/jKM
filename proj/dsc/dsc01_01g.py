# -*- coding: utf-8 -*-
import json

#-- map -----------------------------------------
jsons=[]
replaceList=[]
digits=[str(_) for _ in range(1,101)]
replaceList.append(['"craetedAt":', '"createdAt":'])
replaceList.append(['"created_at":', '"createdAt":'])
replaceList.append(['"session_id":', '"sessionID":'])
replaceList.append(['"user_agent":', '"userAgent":'])
replaceList.append(['"item_id":', '"itemId":'])

drillPaths={
    'payload':1
    ,'payload:itemId':0
    , 'payload:marker':0
    , 'payload:popular':1
}

drillPathType={
    'createdAt':'date'
    , 'payload':'1'
    , 'payload:itemId':'num'
    , 'payload:marker':'num'
}

def expand(item, path='', isDrill=False):
    if type(item) is list:
        for _ in dict():
            p=path+'$'+str(_)
            t='list'
            mapOut(p, str(_), t)
            if p in drillPaths:
                d=drillPaths[p]
            else:
                d=isDrill            
            if d:
                expand(_, p, d)
    elif type(item) is dict:
        for k, v in item.items():
            p=path+str(k)
            t='dict'
            mapOut(p, str(v), t)
            if p in drillPaths:
                d=drillPaths[p]
            else:
                d=isDrill
            if d:
                p+=':'
                expand(v, p, d)
    else:
        p=path+str(item)
        t=str(type(item)).replace("<type '", "").replace("'>", "")
        mapOut(p, str(item), t)

def mapOut(k, v='', t='', s=''):
    #print(k)    
    #intermediate.append(k)
    if t in ['dict', 'list']:
        s='3'
    if k in drillPathType:
        s=drillPathType[k]
    intermediate.append(k + '\t' + str(v) + '\t' + t + '\t' + str(s))
    

datafile = open(r'D:\Josh\data\DSC01\heckle\web.log.2')
intermediate=[]
for _ in datafile.readlines():
    jsonStr=_.replace('""', '"')
    for _1, _2 in replaceList:
        jsonStr = jsonStr.replace(_1, _2)
    jsons.append(json.loads(jsonStr))
    expand(json.loads(jsonStr), '')

#-- /map -----------------------------------------

#-- reduce -----------------------------------------

summary={}
for _ in intermediate:
    _key, _value, _type, _summary=_.split('\t')
    
    if _key not in summary:
        summary[_key]={'cnt':1}
    else:
        summary[_key]['cnt']+=1
        
    summary[_key]['type']=_type
    summary[_key]['summary']=_summary
    #if _type.isdigit():
    if _summary in digits:
        if 'example' not in summary[_key]:
            summary[_key]['example']=[_value]
        else:
            if len(summary[_key]['example'])<int(_summary):
                summary[_key]['example'].append(_value)
    
    if _summary in ['num']:       
        try:
            _value = float(_value)
        except ValueError:
            pass
        if _value==int(_value):
            _value=int(_value)

        if 'min' not in summary[_key]:
            summary[_key]['min']=_value
        else:
            summary[_key]['min']=min(summary[_key]['min'], _value)
        if 'max' not in summary[_key]:
            summary[_key]['max']=_value
        else:
            summary[_key]['max']=max(summary[_key]['max'], _value)
        if 'sum' not in summary[_key]:
            summary[_key]['sum']=_value
        else:
            summary[_key]['sum']+=_value
        if 'avg' not in summary[_key]:
            summary[_key]['avg']=_value
        else:
            summary[_key]['avg']=float(summary[_key]['sum'])/float(summary[_key]['cnt'])

    if _summary in ['date']:
        if 'min' not in summary[_key]:
            summary[_key]['min']=_value
        else:
            summary[_key]['min']=min(summary[_key]['min'], _value)
        if 'max' not in summary[_key]:
            summary[_key]['max']=_value
            
for k, v in sorted(summary.items()):
    vf=''
    t=str(v.pop('type'))
    s=str(v.pop('summary'))
    if t in ['list', 'dict']:
        t='(' + t + '<' + s + '>)'
    else:
        t='(' + t + ')'        

    if 'cnt' in v:    
        c=''+str(v.pop('cnt'))
    for k2, v2 in sorted(v.items()):
        vf+='\t'+str(k2)+':'+str(v2)
    print(c + '\t'+ str(k) + '\t' + t + vf)

#-- /reduce -----------------------------------------
