# -*- coding: utf-8 -*-

class Freq:
            
            


import pandas as pd
df=pd.DataFrame({'a':['a', 'b', 'c', 'adsafaskdjf;lkasdf;aiejfieowj', 'a']})

freq=df['a'].value_counts()
freq.sort()
freq.plot(kind='barh')

