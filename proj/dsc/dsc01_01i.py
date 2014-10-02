#!/usr/bin/python

'''
p = path
t = type
s = summary
'''

import json
import sys
import collections

digits=[str(_) for _ in range(1,101)]

def getReplaceList():
    replaceList=[]
    replaceList.append(['""', '"'])
    replaceList.append(['"craetedAt":', '"createdAt":'])
    replaceList.append(['"created_at":', '"createdAt":'])
    replaceList.append(['"session_id":', '"sessionID":'])
    replaceList.append(['"user_agent":', '"userAgent":'])
    replaceList.append(['"item_id":', '"itemId":'])
    return replaceList

def getDrillPaths():
    return {
        '/auth':0
        , '/createdAt':0
        , '/payload':1
        , '/refId':0
        , '/sessionID':0
        , '/type':1
        , '/user':0
        , '/userAgent':0
        , '/payload/itemId':0
        , '/payload/marker':0
        , '/payload/popular':1
        , '/payload/recent':0
        , '/payload/recommended':0
        , '/payload/results':0

    }

def getPathTypes():    
    return {
        '/auth':'3'
        , '/createdAt':'date'
        , '/payload':'1'
        , '/refId':'3'
        , '/sessionID':'3'
        , '/type':'3'
        , '/user':'num'
        , '/userAgent':'1'
        , '/payload/itemId':'num'
        , '/payload/marker':'num'
        , '/payload/popular':'1'
        , '/payload/popular/':'freq'
        , '/payload/recent':'1'
        , '/payload/recommended':'1'
        , '/payload/results':'1'
    }    

def expand(item, path=''):
    drillPaths=getDrillPaths()
    if type(item) is dict:
        for k, v in item.items():
            p=path + '/' + str(k)
            t='dict'
            mapOut(p, str(v), t)
            d=drillPaths[p] if p in drillPaths else False
            if d: 
                expand(v, p)
                
    elif type(item) is list:
        for _ in item:
            p=path+'/'
            t='list'
            mapOut(p, str(_), t)
            d=drillPaths[p] if p in drillPaths else False
            if d: 
                expand(v, p)
    else:
        p=path+'/'+str(item)
        t=str(type(item)).replace("<type '", "").replace("'>", "")
        mapOut(p, str(item), t)

def mapOut(k, v='', t='', s='', env='local'):
    pathTypes=getPathTypes()
    if t in ['dict', 'list']:
        s='3'
    if k in pathTypes:
        s=pathTypes[k]
    out=k + '\t' + str(v) + '\t' + t + '\t' + str(s)
    if env=='local':
        intermediate.append(out)
    elif env=='mr':
        print(out)
    
    
def mapper(env='local'):
    replaceList=getReplaceList()
    if env=='local':
        datafile = open(inputFile)
        it=datafile.readlines()
    elif env=='mr':
        it=sys.stdin
    for jsonStr in it:
        for r1, r2 in replaceList:
            jsonStr = jsonStr.replace(r1, r2)
        expand(json.loads(jsonStr), '')
        exit

def reducer2(env='local'):
    fields=[]
    for _ in intermediate:
        fields.append(_.split('\t'))
    freq=sorted(collections.Counter([_[0] for _ in fields]).items())
    for _ in freq:
        print('%d\t%s' %(_[1], _[0]))

def reducer(env='local'):
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
            else:
                summary[_key]['max']=max(summary[_key]['max'], _value)

        if _summary in ['freq']:
            if 'freq' not in summary[_key]:
                summary[_key]['freq']={}
                summary[_key]['freq'][_value]=1
            else:
                if _value not in summary[_key]['freq']:
                    summary[_key]['freq'][_value]=1
                else:
                    summary[_key]['freq'][_value]+=1

                
    for k, v in sorted(summary.items()):
        vf=''
        t=str(v.pop('type'))
        s=str(v.pop('summary'))
        if t in ['list', 'dict']:
            t='(' + t + ', ' + s + ')'
        else:
            t='(' + t + ')'        
    
        if 'cnt' in v:    
            c=''+str(v.pop('cnt'))
        for k2, v2 in sorted(v.items()):
            vf+='\t'+str(k2)+':'+str(v2)
        print(c + '\t'+ str(k) + '\t' + t + vf)



env='mr'
if env=='local':
    inputFile=r'D:\Josh\data\DSC01\heckle\web.log.2'
    intermediate=[]
    mapper('local')
    reducer('local')
elif env=='mr':
    if sys.argv[0]=='-m':
        mapper('mr')
    elif sys.argv[0]=='-r':
        reducer('mr')

'''

hadoop fs -rmr /tmp/dsc01_01i

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_01i \
-file /home/biadmin/josh/script/dsc01/dsc01_01i.py \
-mapper "/home/biadmin/josh/script/dsc01/dsc01_01i.py -m" \
-reducer "/home/biadmin/josh/script/dsc01/dsc01_01i.py -r"

'''