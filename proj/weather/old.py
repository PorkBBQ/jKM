# -*- coding: utf-8 -*-


import datetime as dt
import time
import json
import pymongo
from urllib2 import urlopen

con=pymongo.Connection()    
db=con.test
wt=db.weatherTest
wt.remove()

#cityCode='6696918' # Taoyuan
#cityCode='1673820' # Kauhsiung
#cityCode='1668399' # Taichung
cityCode='1668341' # Taipei

date_start=dt.datetime(2013,1,1)
date_end=dt.datetime(2013,8,25)

totalDays=(date_end-date_start).days

oneDay=dt.timedelta(days=1)

for i in range(totalDays):
    print(i)
    
    d1=time.mktime((date_start+oneDay*i).timetuple())
    d2=time.mktime((date_start+oneDay*(i+1)).timetuple())
    
    urlStr=''.join([
        'http://api.openweathermap.org/data/2.1/history/city/'
        , cityCode
        , '?type=day&start='
        , str(d1)
        , '&end='
        , str(d2)
    ])
    print(urlStr)

    url = urlopen(urlStr)
    
    data=json.load(url)
    
    datalist=data['list']
    
    #print('wt.count', wt.count())
    #print(datalist)
    #print(datalist[0].keys())
    print(d1, time.localtime(d1))
    
    
    for d in datalist:
        print(d)
        wt.insert(d)
        
    print('wt.count', wt.count())
