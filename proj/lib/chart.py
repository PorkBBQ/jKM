# -*- coding: utf-8 -*-

def getBarh(values, labels, title='', showData=True):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(16, 12))
    y_pos=range(len(values))
    
    plt.barh(y_pos, values, align='center', alpha=0.5)
    plt.yticks(y_pos, labels)
    plt.title(title)
    if showData:
        for i in y_pos:
            plt.text(values[i], i, ' '+str(values[i]))
    plt.ylim((-1, len(values)))
    
    return plt

def getGeoMap(geos, kmeans_k=1):
    import matplotlib.pyplot as plt
    from scipy.cluster.vq import kmeans2
    import numpy as np
    import proj.silkyfowl as sf
    dots=['or', 'om', 'oc', 'oy', 'ow']
    
    w=1199
    h=600
    
    def locTran(x,y,w=1199,h=600):
        return (float(x+180)*w/360, h-float(y+90)*h/180)
    
    mapCoords=[locTran(geo[1], geo[0]) for geo in geos]
    im = plt.imread(r'rsc\img\world_map.png')
    plt.figure(figsize=(16, 10))
    plt.imshow(im)
    
    if kmeans_k>1:
        #centroids, groups=kmeans2(np.array(mapCoords), kmeans)
        kmeans=sf.KMeans(np.array(mapCoords), kmeans_k)
        centroids=kmeans.getCentroids()
        groups=kmeans.getGroups()
        stdevs=kmeans.getStdevs()

        for i in range(len(mapCoords)):
            plt.plot(mapCoords[i][0], mapCoords[i][1], dots[groups[i]], alpha=0.5,markersize=8)
    
        for i in range(kmeans_k):
            plt.plot(centroids[i][0], centroids[i][1], dots[i%kmeans_k], alpha=0.2,markersize=stdevs[i]*15)
    else:
        for i in range(len(geos)):
            a, b=locTran(geos[i][1], geos[i][0])
            plt.plot(mapCoords[i][0], mapCoords[i][1], dots[0], alpha=0.5,markersize=8)

    #plt.plot(xSeries, ySeries, 'or', alpha=0.5,markersize=8)
    plt.xlim((0,w))
    plt.ylim((h,0))
    plt.yticks(range(0,601,100), [u'90° N', u'60° N', u'30° N', u'0°', u'30° S', u'60° S', u'90° S'], size=8)
    plt.xticks([0, 200, 400, 600, 800, 1000, 1199], [u'180°', u'120° W', u'60° W', u'0°', u'60° E', u'120° E', u'180°'], size=8 )
    plt.show()
    return plt


    import matplotlib.pyplot as plt
    import proj.hairycrab.twitter as hctw
    
    dd=dict()
    for tweet in self.tweets:
        date=hctw.created_at2datetime(tweet['created_at']).date()
        if date in dd.keys():
            dd[date]+=1
        else:
            dd[date]=1
    dd.keys()
    dd.values()

def getChartDaily(dates):
    import matplotlib.pyplot as plt
    import proj.lib.freq as freq
    dd=dict()
    
    days=[_.date() for _ in dates]
    dayFreq=freq.getFreq(days)
    
    values=[_[1] for _ in dayFreq]
    labels=[_[0] for _ in dayFreq]    
    label_ticks=[_.strftime('%Y-%m-%d') for _ in labels]
    plt.figure(figsize=(16, 12))
    plt.bar(labels, values, align='center', alpha=0.5)
    
    plt.xticks(labels, label_ticks, rotation=280)
    
    for i in range(len(labels)):
        plt.text(labels[i], values[i], values[i], va='baseline', ha='center')
    return plt
    plt.figure(figsize=(16, 12))
    plt.bar(dd.keys(), dd.values(), align='center', alpha=0.5)
    dateStr=[_.strftime('%Y-%m-%d') for _ in dd.keys()]
    plt.xticks(dd.keys(), dateStr, rotation=280)
    for i in range(len(dd.keys())):
        plt.text(dd.keys()[i], dd.values()[i], dd.values()[i], va='baseline', ha='center')
    return plt

def getChartBarOrdinal(values, ordinals, title='', showData=True):
    import matplotlib.pyplot as plt
    
    dct={}
    for i in range(len(values)):
            dct[ordinals[i]]=values[i]
    
    dataOrdinal=[]
    labels=range(min(dct.keys()), max(dct.keys())+1)
    for i in labels:
        if i in dct:
            dataOrdinal.append(dct[i])
        else:
            dataOrdinal.append(0)
    plt.figure(figsize=(16, 12))
    plt.bar(labels, dataOrdinal, align='center')
    if showData:
        for i in range(len(values)):
            plt.text(ordinals[i], values[i], values[i], va='baseline', ha='center', alpha=0.5)
    return plt

def getChartAccu(values):
    import matplotlib.pyplot as plt
    newValues=[values[0]]
    for i in range(1,len(values)):
        newValues.append(newValues[i-1]+values[i])
    plt.plot(newValues)
    return plt
