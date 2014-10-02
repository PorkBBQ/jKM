# -*- coding: utf-8 -*-
"""
Created on Sun Dec 08 18:26:00 2013

@author: 1309075
"""

class Freq():
    
    lst=[]
    def __init__(self, lst=[], freq=[[]]):
        if freq==[[]]:
            self.freq=self.getFreq(lst)
        else:
            self.freq=freq

    def getFreq(self, count=20, minCount=0, proportion=False):
        d=dict()
        for item in self.lst:
            if item in d:
                d[item]+=1
            else:
                d[item]=1
        sortDesc=sorted([(v, k) for (k, v) in d.items()], reverse=True)
        freq=[[k, v] for [v, k] in sortDesc if v>=minCount]
        if proportion==False:
            return freq
        else:
            total=sum([f[1] for f in freq])
            for f in freq:
                f.append(float(f[1])/total)
            return freq
    
    def getFreqTable(self, lstName='Item' , tableName='LstFreqTable', proportion=False):
        freqLst=self.getFreq(self.lst, proportion=proportion)
        return self.getTable(freqLst, freqName=lstName , tableName=tableName, proportion=proportion)
            
    def getFreqChart(self, kind='barh', count=20, minCount=0):
        import proj.lib.chart as jChart
        freqLst=self.getFreq(self.lst)
        values=[_[1] for _ in freqLst][:count][::-1]
        labels=[_[0] for _ in freqLst][:count][::-1]
        return jChart.getChartBarh(values, labels)

    def getTable(freqLst, freqName='Item' , tableName='LstFreqTable', proportion=False):
            table='<table name="' + tableName + '">'
            table+='<tr><th>'+ freqName +'</th><th>Count</th>'
            if proportion:
                table+='<th>Rate</th>'
            table+='</tr>'
            for _ in freqLst:
                table+='<tr>'            
                for i in range(len(_)):
                    table+='<td>'
                    if i==2:
                        table+='%0.2f%%'%(_[i]*100)
                    else:
                        try:
                            table+=str(_[i]).decode('ascii', 'ignore')
                        except UnicodeEncodeError:
                            print('=== Oops, UnicodeEncodeError! ===')
                            print(_[i].encode('utf8', 'ignore'))
                    
                    table+='</td>'
                table+='</tr>'
            table+='</table>'
            return table
    
