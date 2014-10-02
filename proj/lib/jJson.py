# -*- coding: utf-8 -*-

def getSubDictByKeys(dct, keys=[]):
    subDict={}
    for k, v in dct.items():
        if k in keys:
            subDict[k]=v
    return subDict

def getKVs(dctItems, pathStr):
    at=pathStr.find('.')
    if at==-1:
        cur=pathStr
        remain=''
    else:
        cur=pathStr[0:at]
        remain=pathStr[at+1:]

    if cur=='': #if '', return current data
        return dctItems
        
    elif cur=='*': #if '*', recur all elements
        newDctItems=[]
        for k, v in dctItems:
            for item in v:
                newDctItems.append([k, item])
        return getKVs(newDctItems, remain)
        
    elif cur!='*': #if not '*', drill down subElement
        newDctItems=[]
        for k, v in dctItems:
            if type(v)==type({}) and cur in v:
                newDctItems.append([k, v[cur]])
        return getKVs(newDctItems, remain)

       
        
def getItems(jsons, items):
    results=[]
    for json in jsons:
        result=[]
        for item in items:
            obj=json
            for section in item.split('.'):
                if section in obj:
                    obj=obj[section]
                else:
                    obj=None
            result.append(obj)

        if len(items)==1:
            results.append(result[0])
        else:
            results.append(result)
    return results

def unpivot(rows=[]):
    if type(rows)==type({}):
        rows=rows.items()
    unpvt=[]
    for row in rows:
        for col in row[1]:
            unpvt.append([row[0], col])
    return unpvt

def pivot(kvs=[], rtn='list'):
    pvt={}
    for k, v in kvs:
        if k in pvt:
            pvt[k].append(v)
        else:
            pvt[k]=[v]
    if rtn=='list':
        pvt=pvt.items()
    return pvt

def getSubDict(dct, k, v, operator='eq'):
    subDict={}
    for dct_k, dct_v in dct.items():
        o=dct_v
        for element in k.split('.'):
            if element in o:
                o=o[element]
            else:
                exit
        if operator=='eq':
            if o==v:
                subDict[dct_k]=dct_v
        if operator=='!eq':
            if o!=v:
                subDict[dct_k]=dct_v
        if operator=='gt':
            if o>v:
                subDict[dct_k]=dct_v
        if operator in ['gte', '!lt']:
            if o>=v:
                subDict[dct_k]=dct_v
        if operator=='lt':
            if o<v:
                subDict[dct_k]=dct_v
        if operator in ['lte', '!gt']:
            if o<=v:
                subDict[dct_k]=dct_v
        if operator=='in':
            if o in v:
                subDict[dct_k]=dct_v
        if operator=='!in':
            if not o in v:
                subDict[dct_k]=dct_v
        if operator=='contain':
            if v in o:
                subDict[dct_k]=dct_v
        if operator=='!contain':
            if not v in o:
                subDict[dct_k]=dct_v
    return subDict
