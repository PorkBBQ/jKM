
# -*- coding: utf-8 -*-

class Tweets:
    def __init__(self, raws=[], docs={}):
        if docs=={}:
            self.raws=raws
            #self.meta=meta
            self.docs={}       
            for raw in raws:
                doc={}
                doc['meta']={}
                doc['raw']=raw
                doc['stat']={}
                doc['anno']={}
                self.docs[raw['id']]=doc
        else:
            self.docs=docs
            self.raws=[]
            self.wc=[]
            for doc in docs.values():
                self.raws.append(doc['raw'])
        self.metas={
            'created_at':'raw.created_at'
            , 'geo':'raw.geo.coordinates'
            , 'lang':'raw.lang'
            , 'hashtags':'raw.entities.hashtags.*.text'
            , 'source':'raw.source'
            , 'domains':'stat.domains'
            , 'expanded_urls':'raw.entities.urls.*.expanded_url'
            , 'mentions_id':'raw.entities.user_mentions.*.id'
            , 'mentions_name':'raw.entities.user_mentions.*.name'
            , 'display_domains':'raw.entities.urls.*.display_url'
            , 'in_reply_to_screen_name':'raw.in_reply_to_screen_name'
            , 'favorite_count':'raw.favorite_count'
            , 'retweet_count':'raw.retweet_count'
            , 'user_description':'raw.user.description'
            , 'user_id':'raw.user.id'
            , 'user_name':'raw.user.name'
            , 'user_favourites_count':'raw.user.favourites_count'
            , 'user_followers_count':'raw.user.followers_count'
            , 'user_friends_count':'raw.user.friends_count'
        }

    def getKVs(self, pathStr):
        import proj.lib.jJson as jJson
        return jJson.getKVs(self.docs.items(), pathStr)
        
    def getItems(self, items=[]):
        import proj.lib.jJson as jJson
        return jJson.getItems(self.docs.values(), items)
    
    def getItem(self, pathStr):
        kvs=self.getKVs(pathStr)
        return [_[1] for _ in kvs]

    def getSubDct(self, pathStr):
        subDct={}
        for k, v in self.getKVs(pathStr):
            subDct[k]=v
        return subDct
        
    def getCount(self):
        return len(self.docs.items())
        
    def getStats(self):
        from lib import created_at2datetime
        stats=dict()
        stats['count']=self.getCount()
        stats['userCount']=len(set([raw['user']['id'] for raw in self.raws]))
        stats['minId']=min([raw['id'] for raw in self.raws])
        stats['maxId']=max([raw['id'] for raw in self.raws])
        stats['minTime']=min([created_at2datetime(raw['created_at']) for raw in self.raws])
        stats['maxTime']=max([created_at2datetime(raw['created_at']) for raw in self.raws])
        td=stats['maxTime']-stats['minTime']
        stats['countPerDay']=stats['count']/(float(td.days)+float(td.seconds)/86400)
        return stats
       
    def saveHbase(self, hbase, tableName='test', columnFamily='raw'):
        import proj.lib.jData as jData
        dct={}
        for k, v in self.docs.items():
            dct[k]=v[columnFamily]
        jData.insertHbase(hbase, tableName, columnFamily, dct)
        return 

    def updateWordCount(self, proc='lower', stemMethod='1', minCount=1, batchSize=1000):
        import proj.lib.textAnalysis as ta
        self.wc=ta.getWordCount(self.getItem('raw.text'))
        return

    def getSubset(self, k, v, operator='eq'):
        import proj.lib.jJson as jJson
        subDocs=jJson.getSubDict(dct=self.docs, k=k, v=v, operator=operator)
        return Tweets(docs=subDocs)

    def ss(self, k, v, operator='eq'):
        return self.getSubset(k=k, v=v, operator=operator)

    def getSubsetByKeys(self, keys=[]):
        import proj.lib.jJson as jJson
        subDocs=jJson.getSubDictByKeys(dct=self.docs, keys=keys)
        return Tweets(docs=subDocs)
        
    def updateStat(self):
        import re
        import proj.lib.jJson as jJson
        
        statLst=self.metas.copy()
        statLst.pop('domains')
        
        # get raw items
        stats_1={}
        for k, v in statLst.items():
            stats_1[k]=self.getKVs(v)
        
        # get stemed
        stats_2=stats_1.copy()
        for _ in stats_2['hashtags']:_[1]=u'#'+_[1].lower()
        for _ in stats_2['mentions_name']:_[1]=u'@'+_[1].lower()
        for _ in stats_2['display_domains']:_[1]=_[1].split('/')[0]
        for _ in stats_2['source']:_[1]=re.search('>.+</a>', _[1]).group()[1:-4].lower() if re.search('>.+</a>', _[1]) else _[1]
        #for _ in metas_2['created_at']:_[1]=hctw.created_at2datetime(_[1])
        
        # get pivoted
        stats_3=stats_2.copy()
        for stat in ['display_domains', 'hashtags', 'expanded_urls', 'mentions_id', 'mentions_name']:
            stats_3[stat]=jJson.pivot(stats_3[stat])
                
        # update cell by cell
        for statName, stat in stats_3.items():
            for k, v in stat:
                self.docs[k]['stat'][statName]=v

        return
        
    def updateStatDomains(self):
        import proj.lib.internet as internet
        i=0        
        length=self.getCount()
        for _id, doc in self.docs.items():
            i+=1
            domains=[]
            for url in doc['raw']['entities']['urls']:
                eUrl=url['expanded_url']
                print('get domains %d/%d : %s' %(i, length, eUrl))
                domain=internet.getDomain(eUrl)
                domains.append(domain)
            doc['stat']['domains']=domains


    def updateStatDomainsMultiThread(self, threadCount=100):
        import thread 
        length=self.getCount()
        
        batchLength=(length//threadCount)+1        
        docsitems=self.docs.items()

        batches=[]
        nos=[]
        for i in range(threadCount):
            arr=[]
            arr2=[]
            for j in range(i*batchLength, min((i+1)*batchLength, length)):
                arr.append(j)
                arr2.append(docsitems[j][1]['raw']['id'])
            nos.append(arr)
            batches.append(arr2)

        for i in range(len(batches)):
            if len(batches[i])>0:
                thread.start_new_thread(self.updateDomainByIds,(batches[i], nos[i], length))
        #print('Count of raw.entities.urls.*.expanded_url: %d' % len(self.getItem('raw.entities.urls.*.expanded_url')))
        #print('Count of stat.domains.*: %d' % len(self.getItems('stat.domains.*')))
        return

    def updateDomainByIds(self, ids, nos, length):
        import proj.lib.internet as internet
        
        for i in range(len(ids)):
            _id=ids[i]
            no=nos[i]
            domains=[]
            for url in self.docs[_id]['raw']['entities']['urls']:
                eUrl=url['expanded_url']
                domain=internet.getDomain(eUrl)
                domains.append(domain)
                print('get domain %d/%d, %s : %s --> %s' %(no, length ,str(_id), eUrl, domain))
            self.docs[_id]['stat']['domains']=domains
        return domains
            
    def Report(self):
        import report
        return report.Report(self)

    def TextAnalysis(self, maxCount=-1):
        import textAnalysis
        return textAnalysis.TextAnalysis(self, maxCount)
        
# =================================================

    def updateDomainCat(self):
        import proj.albatross as ab
        domainDct=ab.getDict('domains', 'domains')
        cats=set([_[1]['category'] for _ in domainDct.items()])
        for k, v in self.docs.items():
            for cat in cats:
                catDomains=[_[0] for _ in domainDct.items() if _[1]['category']==cat]
                for domain in v['stat']['domains']:
                    self.docs[k]['anno']['domain_is_'+cat]=1 if domain in catDomains else 0

    def getDomainsTable(self):
        import proj.lib.freq as freq
        domains=self.getItem('stat.domains.*')
        return freq.getDomainTable(domains)
            
    def getChartTopHashTags(self, topCount=5):
        import proj.lib.freq as jFreq
        import pandas as pd
        import matplotlib.pyplot as plt
        
        dailyAll=self.getDailyStat(self, 'raw.id', 0L, '!eq')
        hashtags=self.getItem('stat.hashtags.*')
        topHashtags=[_[0] for _ in jFreq.getFreq(hashtags)[:topCount]]
        df=pd.DataFrame(data=[0.0+_[1] for _ in dailyAll], index=[_[0] for _ in dailyAll], columns=['all'])
        
        for hashtag in topHashtags:
            s=self.getDailyStat(self, 'stat.hashtags', hashtag, 'contain')
            df[hashtag]=pd.Series(data=[0.0+_[1] for _ in s], index=[_[0] for _ in s])
            df[hashtag+' rate']=df[hashtag]/df['all']
        
        df=df.fillna(0.0).sort()
        
        rates=[_+' rate' for _ in topHashtags]
        ax = plt.figure(figsize=(16, 12)).add_subplot(111)
        df[rates].plot(ax=ax)
        plt.xticks(rotation=80)
        return plt

    def getChartKeywords(self):
        import proj.lib.freq as jFreq
        import pandas as pd
        import matplotlib.pyplot as plt
        import proj.hairycrab.twitter as hctw
        dailyAll=self.getDailyStat(self, 'raw.id', 0L, '!eq')
        topKeywords=['chromebook', 'touchscreen', 'aspire']
        
        df=pd.DataFrame(data=[0.0+_[1] for _ in dailyAll], index=[_[0] for _ in dailyAll], columns=['all'])
        
        for keyword in topKeywords:
            dates=[hctw.created_at2datetime(_[1]['stat']['created_at']).date() for _ in self.docs.items() if keyword in _[1]['raw']['text'].lower().split()]
            s=jFreq.getFreq(lst=dates)
            df[keyword]=pd.Series(data=[0.0+_[1] for _ in s], index=[_[0] for _ in s])
            df[keyword+' rate']=df[keyword]/df['all']
        
        df=df.fillna(0.0).sort()
        
        rates=[_+' rate' for _ in topKeywords]
        ax = plt.figure(figsize=(16, 12)).add_subplot(111)
        df[rates].plot(ax=ax)
        plt.xticks(rotation=80)
        return plt
        
    def getDailyStat(self, tweets, k, v, operator):
        import proj.lib.jJson as jJson
        import proj.hairycrab.twitter as hctw
        import proj.lib.freq as jFreq
        ss=jJson.getSubDict(dct=tweets.docs, k=k, v=v, operator=operator)
        days=[hctw.created_at2datetime(_['raw']['created_at']).date() for _ in ss.values()]
        daysFreq=jFreq.getFreq(days)
        return daysFreq

    def getApriori(self, minSupport=0.1, minConfinence=0.3
            , keywordList=['chromebook', 'touchscreen', 'aspire', 'laptop', 'computer', 'notebook', 'c720p']):
        import proj.lib.textAnalysis as ta
        
        texts=self.getItem('raw.text')
        dataset=[]
        for _ in texts:
            dataset.append(ta.getTokens(_, keywordList=keywordList))
        apriori=ta.apriori(dataset, minSupport=minSupport, minConfidence=minConfinence, keywordList=[])
        return apriori
