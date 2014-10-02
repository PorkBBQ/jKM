#!/usr/bin/python
import sys

summary={}
for _ in sys.stdin:
    _=_.strip()
    _key, _value, _type=_.split('\t')
    
    if _key not in summary:
        summary[_key]={'cnt':1}
    else:
        summary[_key]['cnt']+=1
        
    #if _type.isdigit():
    if _type in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        if 'example' not in summary[_key]:
            summary[_key]['example']=[_value]
        else:
            if len(summary[_key]['example'])<int(_type):
                summary[_key]['example'].append(_value)
    
    if _type in ['num']:
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

    if _type in ['date']:
        if 'min' not in summary[_key]:
            summary[_key]['min']=_value
        else:
            summary[_key]['min']=min(summary[_key]['min'], _value)
        if 'max' not in summary[_key]:
            summary[_key]['max']=_value
            
for k, v in sorted(summary.items()):
    vf=''
    if 'cnt' in v:    
        vf='\tcnt:'+str(v.pop('cnt'))
    for k2, v2 in sorted(v.items()):
        vf+=', '+str(k2)+':'+str(v2)
    print(str(k)+vf)

