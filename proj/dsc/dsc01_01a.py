# -*- coding: utf-8 -*-

import json

datafile = open(r'D:\Josh\data\DSC01\heckle\web.log.2')

#-- map -----------------------------------------
jsons=[]
for _ in datafile.readlines():
    json_str=_.replace('""', '"')
    jsons.append(json.loads(json_str))
    
for _1 in jsons:
    for _2 in _1.keys():
        print(_2)
#-- /map -----------------------------------------

#-- reduce -----------------------------------------

counter=collections.Counter(intermediate)
for _ in counter.items():
    print(_)
        
#-- /reduce -----------------------------------------


