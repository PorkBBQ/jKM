# -*- coding: utf-8 -*-

def getFreq(lst=[], minFreq=0, proportion=False):
    d=dict()
    for item in lst:
        if item in d:
            d[item]+=1
        else:
            d[item]=1

    sortDesc=sorted([(-v, k) for (k, v) in d.items()])
    sortDesc2 = [(k, -v) for (v, k) in sortDesc]
    freq=[[k, v] for [k, v] in sortDesc2 if v>=minFreq]
    
    if proportion==False:
        return freq
    else:
        total=sum([f[1] for f in freq])
        for f in freq:
            f.append(float(f[1])/total)
        return freq

def printFreq(lst=[], kind='barh', freq=[[]]):
    if freq==[[]]:
        freq=getFreq(lst)
    
    for row in freq:
        p=''
        for ele in row:
            p+=str(ele) + u'\t'
        print(p)
    
def getFreqChart(lst=[], kind='barh', count=30, minFreq=0, title='', freq=[[]]):
    import proj.lib.chart as jChart
    if freq==[[]]:
        freq=getFreq(lst, minFreq=minFreq)
    values=[_[1] for _ in freq][:count][::-1]
    labels=[_[0] for _ in freq][:count][::-1]
    return jChart.getBarh(values, labels, title=title)

def getFreqChartAccu(lst=[], kind='barh', count=30, minFreq=0, title='', freq=[[]]):
    return
    
def getFreqTable(lst=[], freqName='Item' , tableName='LstFreqTable', count=500, minFreq=0, noColumn=False, proportion=False, freq=[[]]):
    if freq==[[]]:
        freq=getFreq(lst, minFreq=minFreq, proportion=proportion)
            
    table='<table name="' + tableName + '"><tr>'
    if noColumn:
        table+='<th>No</th>'
    table+='<th>'+ freqName +'</th><th>Count</th>'
    if proportion:
        table+='<th>Rate</th>'
    table+='</tr>'
    cnt=0
    for _ in freq[:count]:
        cnt+=1
        table+='<tr>'            
        if noColumn:
            table+='<td>%d</td>' % cnt
        for i in range(len(_)):
            table+='<td>'
            if proportion and i==2:
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


#==============================================================================

def getDomainTable(domains):
    import proj.albatross as ab
    import proj.lib.freq as freq

    dctDomain=ab.getDict('domains', 'domains')

    freqDomain=freq.getFreq(domains)
    joined=[]
    for _ in freqDomain:
        k=_[0]
        v=_[1]
        lst=[k]
        if k in dctDomain:
            lst.append(dctDomain[k]['category'])
            idTech='Y' if dctDomain[k]['isTech']==1 else 'N'
            lst.append(idTech)
        else:
             lst.append('')
             lst.append('')
        lst.append(v)
        joined.append(lst)

    total=sum([_[3] for _ in joined])            
    for _ in joined:_
    table='<table>'
    table+='<tr><th>Domain</th><th>Category</th><th>IsTech</th><th>Count</th><th>Rate</th></tr>'
    for _ in joined:
        lnk='<a href="http://%s" target="_blank">%s</a>' % (_[0], _[0])
        table+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%d</td><td>%.2f%%</td></tr>' %(lnk, _[1], _[2], _[3], float(_[3])/total*100)
    table+='</table>'
    return table