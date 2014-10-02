#!/home/biadmin/anaconda/bin/python

import json
import sys

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
        , '/payload/recommended':1
        , '/payload/recs/':1
        , '/payload/results':1
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
        , '/payload/lengtg':'num'
        , '/payload/marker':'num'
        , '/payload/new':'freq10'
        , '/payload/old':'freq10'
        , '/payload/popular':'1'
        , '/payload/popular/':'freq10'
        , '/payload/rating':'freq10'
        , '/payload/recent':'3'
        , '/payload/recs':'3'
        , '/payload/recs/':'freq10'
        , '/payload/recommended':'3'
        , '/payload/recommended/':'freq10'
        , '/payload/results':'1'
        , '/payload/results/':'freq10'
    }   

def expand(item, path='', gPath='type'):
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

def mapOut(k, v='', t='', s=''):
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

def mapper(env):
    if env=='local':
        datafile = open(inputFile)
        it=datafile.readlines()
    elif env=='mr':
        it=sys.stdin
    for _ in it:
        _ = _.strip()
        for r1, r2 in getReplaceList():
            _ = _.replace(r1, r2)
        expand(json.loads(_))

def reducer(env='local'):
    summary={}
    if env=='local':
        it=intermediate 
    elif env=='mr':
        it=sys.stdin
    for _ in it:
        _key, _value, _type, _summary=_.split('\t')
        _key=_key.strip()
        _value=_value.strip()
        _type=_type.strip()
        _summary=_summary.strip()
        
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

        if _summary in ['freq', 'freq10']:
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
        if s=='freq10':
            v['freq']=sorted(v['freq'].items(), key=lambda x:x[1], reverse=True)[:10]
        for k2, v2 in sorted(v.items()):
            vf+='\t'+str(k2)+':'+str(v2)
        print(c + '\t'+ str(k) + '\t' + t + vf)

env='local' if len(sys.argv)==1 else 'mr'

if env=='local':
    inputFile=r'D:\Josh\data\DSC01\heckle\web.log.2'
    intermediate=[]
    mapper('local')
    reducer('local')
elif env=='mr':
    if sys.argv[1]=='-m':
        mapper('mr')
    elif sys.argv[1]=='-r':
        reducer('mr')


'''

hadoop fs -rmr /tmp/dsc01_02b

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_01b' \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_02b \
-file /home/biadmin/josh/script/dsc01/dsc01_02b.py \
-mapper "/home/biadmin/josh/script/dsc01/dsc01_02b.py -m" \
-reducer "/home/biadmin/josh/script/dsc01/dsc01_02b.py -r"

'''
