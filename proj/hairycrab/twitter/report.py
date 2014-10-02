
# -*- coding: utf-8 -*-
class Report:
    def __init__(self, tweets, PYTHON_HOME=r'D:\Josh\Dropbox\Python', TEMP_HOME=r'proj\hairycrab\twitter\report\temp', DOC_HOME=r'proj\hairycrab\twitter\report'):
        self.tweets=tweets
        self.PYTHON_HOME=PYTHON_HOME
        self.TEMP_HOME=TEMP_HOME
        self.DOC_HOME=DOC_HOME
        
    def geneReport(self, chapters='_all', name='tweets', title='Tweets'):
        import proj.jChm as jChm
        import proj.lib.chm as lChm
        import shutil
        
        if chapters=='_all':
            chapters=['stats', 'freqs', 'trends', 'classify', 'ta', 'users']

        chm=jChm.Chm(name)
        chm.paras['path']=self.TEMP_HOME
        chm.paras['title']=title
        
        # cover
        cover=lChm.getCover(title=title, fileName='_cover', TEMP_HOME=self.TEMP_HOME)
        chm.addPage(cover)
        
        if 'stats' in chapters:
            for page in self.geneReportStats():
                chm.addPage(page)

        if 'summary' in chapters:
            for page in self.geneReportSummary():
                chm.addPage(page)

        if 'freqs' in chapters:
            for page in self.geneReportFreqs():
                chm.addPage(page)

        if 'trends' in chapters:
            for page in self.geneReportTrends():
                chm.addPage(page)

        if 'classify' in chapters:
            for page in self.geneReportClassify():
                chm.addPage(page)

        if 'ta' in chapters:
            for page in self.geneReportTa():
                chm.addPage(page)
        
        if 'users' in chapters:
            for page in self.geneReportUsers():
                chm.addPage(page)
            
        print(chm.generateAll())                    
        shutil.copyfile(self.TEMP_HOME+'\\'+name+'.chm', self.DOC_HOME+'\\'+name+'.chm')
        print('copy to --> '+self.PYTHON_HOME+'\\'+self.DOC_HOME+'\\'+name+'.chm')
        return


        
    def geneReportStats(self):
        import proj.lib.chart as jChart
        import proj.lib.chm as lChm
        import proj.hairycrab.twitter as hctw 
        
        #meta
        title=dict()
        title['stats']='Statistics'
        title['daily']='Daily Distribution'
        title['geoMap']='Grographic Distribution'
        title['geoMapCluster']='Grographic Distribution - clustered'
        
        desc=dict()
        desc['stats']='Some basic statistics of the tweets'
        desc['daily']='Daily distribution of tweet created time'
        desc['geoMap']='The locations that tweets was posted from, may not available for every tweet'
        desc['geoMapCluster']='Clustered GeoMap'
        
        #data
        data={}
        data['stats']=self.tweets.getStats()
        data['daily']=[hctw.created_at2datetime(_) for _ in self.tweets.getItem('stat.created_at')]
        data['geoMap']=self.tweets.getItem('stat.geo')
        data['geoMapCluster']=self.tweets.getItem('stat.geo')
        
        # Daily Chart
        plt=jChart.getChartDaily(data['daily'])
        plt.savefig(self.TEMP_HOME+r'\daily.png')

        # Geo Chart
        plt=jChart.getGeoMap(data['geoMap'])
        plt.savefig(self.TEMP_HOME+r'\geoMap.png')

        # Geo ChartCluster
        try:
            plt=jChart.getGeoMap(data['geoMap'], 3)
            plt.savefig(self.TEMP_HOME+r'\geoMapCluster.png')
        except Exception:
            plt=jChart.getGeoMap(data['geoMap'])
            plt.savefig(self.TEMP_HOME+r'\geoMapCluster.png')
        
        content=dict()
        content['stats']=''
        content['stats']+='<table><tr><th>Stat</th><th>Value</th></tr><tr>'
        for stat in ['count', 'userCount', 'minTime', 'maxTime', 'minId', 'maxId', 'countPerDay']:
            content['stats']+='<tr><td>%s</td><td>%s</td></tr>' % (stat, str(data['stats'][stat]))
        content['stats']+='</table>'
        
        content['daily']='<img src="daily.png" width="800" height="600" />'
        content['geoMap']='<img src="geoMap.png" width="1600" />'
        content['geoMapCluster']='<img src="geoMapCluster.png" width="1600" />'
        
        pages=[]
        for page in ['stats', 'daily', 'geoMap']:
            p=lChm.getTemplate1(name=page, title=title[page], desc=desc[page], fileName=page, parentName='cover', TEMP_HOME=self.TEMP_HOME, content=content[page])
            pages.append(p)
        page='geoMapCluster'
        p=lChm.getTemplate1(name=page, title=title[page], desc=desc[page], fileName=page, parentName='geoMap', TEMP_HOME=self.TEMP_HOME, content=content[page])
        pages.append(p)
        return pages
        
    def geneReportSummary(self):
        import proj.lib.chart as jChart
        import proj.lib.chm as lChm
        import proj.hairycrab.twitter as hctw

        subjects=[]
        title=dict()
        title['lang']='Languages'
        
        desc=dict()
        desc['lang']='Languages Distribution'

        contents=[]
        for subject in subjects:
            contents.append([title[subject], desc[subject], subject])
        pages=[]        
        pages.append(lChm.getChapterHead(name='summary', title='Summary', fileName='summary', parentName='cover', TEMP_HOME=self.TEMP_HOME, contents=contents))
        for page in subjects:
            p=lChm.getTemplate1(name=page, title=title[page], desc=desc[page], fileName=page, parentName='summary', TEMP_HOME=self.TEMP_HOME, content=content[page])
            pages.append(p)
        return pages
        
    def geneReportFreqs(self):
        import proj.lib.chm as lChm
        import proj.lib.freq as jFreq
        
        # meta
        subjects=['lang', 'source', 'hashtags', 'mentions_name', 'domains', 'display_domains'
            , 'favorite_count', 'retweet_count'
            , 'user_id', 'user_favourites_count', 'user_followers_count', 'user_friends_count']
        title=dict()
        title['lang']='Languages'
        title['source']='Sources'
        title['hashtags']='HashTags'
        title['mentions_name']='Mentioned User Name'
        title['domains']='Domains'
        title['display_domains']='Display Domains'
        title['favorite_count']='Favorate Count'
        title['retweet_count']='Retweet Count'
        title['user_id']='User Id Count'
        title['user_favourites_count']='User Favorate Count'
        title['user_followers_count']='User Follower Count'
        title['user_friends_count']='User Friends Count'
        
        desc=dict()
        desc['lang']='Languages Distribution'
        desc['source']='Sources, can be website or app'
        desc['hashtags']='HashTags in the tweets'
        desc['mentions_name']='User name mentioned in tweets'
        desc['domains']='Domains of Urls in the tweets'
        desc['display_domains']='Display Domains of Urls'
        desc['favorite_count']='Favorite Count'
        desc['retweet_count']='Retweet Count'
        desc['user_id']='User Id Count (Top 100)'
        desc['user_favourites_count']='User Favorite Count'
        desc['user_followers_count']='Count of Friends (people who is following user)'
        desc['user_friends_count']='Count of followers (people who is followed by user)'

        # data
        data={}
        for subject in subjects:
            if subject in ['hashtags', 'domains', 'display_domains', 'mentions_name']:
                data[subject]=self.tweets.getItem('stat.'+subject+'.*')
            else:
                data[subject]=self.tweets.getItem('stat.'+subject)
        
        # chart
        chart={}
        for subject in subjects:
            plt=jFreq.getFreqChart(data[subject], title=title[subject])
            plt.savefig('%s\%s.png' % (self.TEMP_HOME, subject))
            chart[subject]='<img src="%s.png" width="800" height="600" />' % subject
        
        # table
        table={}
        for subject in subjects:
            if subject=='domains':
                table[subject]=self.tweets.getDomainsTable()
            elif subject=='user_id':
                userFreq=jFreq.getFreq(data[subject], proportion=True)[:100]
                t='<table><tr><th>Item</th><th>Count</th></tr>'
                for _ in userFreq:
                    t+='<tr><td><a href="%s.html">%s</a></td><td>%d</td></tr>' %(str(_[0]), str(_[0]), _[1])
                t+='</table>'
                table[subject]=t
            else:
                table[subject]=jFreq.getFreqTable(data[subject], proportion=True)
            
        content=dict()
        for subject in subjects:
            content[subject]='<table style="border-style:none"><tr><td style="border-style:none;text-align:left;vertical-align:top">%s</td><td style="border-style:none;text-align:left;vertical-align:top">%s</td></tr></table>' % (table[subject], chart[subject])
        
        contents=[]
        for subject in subjects:
            contents.append([title[subject], desc[subject], subject])
        pages=[]        
        pages.append(lChm.getChapterHead(name='freqs', title='Frequency Statistics', fileName='freqs', parentName='cover', TEMP_HOME=self.TEMP_HOME, contents=contents))
        for page in subjects:
            p=lChm.getTemplate1(name=page, title=title[page], desc=desc[page], fileName=page, parentName='freqs', TEMP_HOME=self.TEMP_HOME, content=content[page])
            pages.append(p)
        return pages

    def geneReportTrends(self):
        import proj.lib.chart as jChart
        import proj.lib.chm as lChm
        import proj.hairycrab.twitter as hctw 

        subjects=['hashtagsTrend', 'keywordsTrend']
        title=dict()
        title['hashtagsTrend']='Hashtags Trend'
        title['keywordsTrend']='Keywords Trend'
        
        desc=dict()
        desc['hashtagsTrend']='Top 5 hashtags trend'
        desc['keywordsTrend']='Custom keywords trend'

        table=dict()
        table['']=''
        
        chart=dict()
        subject='hashtagsTrend'
        plt=self.tweets.getChartTopHashTags(5)
        plt.savefig('%s\%s.png' % (self.TEMP_HOME, subject))
        chart[subject]='<img src="%s.png" width="800" height="600" />' % subject

        subject='keywordsTrend'
        plt=self.tweets.getChartKeywords()
        plt.savefig('%s\%s.png' % (self.TEMP_HOME, subject))
        chart[subject]='<img src="%s.png" width="800" height="600" />' % subject
        
        content=dict()
        content['hashtagsTrend']=chart['hashtagsTrend']
        content['keywordsTrend']=chart['keywordsTrend']
        
        contents=[]
        for subject in subjects:
            contents.append([title[subject], desc[subject], subject])
        pages=[]        
        pages.append(lChm.getChapterHead(name='trends', title='Trends', fileName='trends', parentName='cover', TEMP_HOME=self.TEMP_HOME, contents=contents))
        for page in subjects:
            p=lChm.getTemplate1(name=page, title=title[page], desc=desc[page], fileName=page, parentName='trends', TEMP_HOME=self.TEMP_HOME, content=content[page])
            pages.append(p)
        return pages

    def geneReportClassify(self):
        import proj.lib.chart as jChart
        import proj.lib.chm as lChm
        import proj.hairycrab.twitter as hctw 
        import proj.lib.freq as jFreq
        from proj.lib.others import cart_20131221
        
        subjects=['advert']
        title=dict()
        title['advert']='Advertising'
        
        desc=dict()
        desc['advert']='Classification for Advertising'

        # This is not supposed to be here ================================================================
        cartData={}
        for item in self.tweets.docs.items():
            domain_eCommerce=0
            text_at=0
            text_shipping=0
            if 'www.ebay.com' in item[1]['stat']['domains'] or 'www.amazon.com' in item[1]['stat']['domains']:
                domain_eCommerce=1
            if '@' in item[1]['raw']['text']:
                text_at=1
            if 'shipping' in item[1]['raw']['text']:
                text_shipping=1
            cartData[item[0]]=[domain_eCommerce, text_at, text_shipping]
        cartResult={}
        for item in cartData.items():
            cartResult[item[0]]='Advert' if cart_20131221(item[1][0], item[1][1], item[1][2])==1 else 'Non-Advert'
        #===============================================================================================
    
        table=dict()
        subject='advert'
        table[subject]=jFreq.getFreqTable([_[1] for _ in cartResult.items()], proportion=1)
        
        chart=dict()
        subject='advert'
        #chart[subject]=freq.getFreqChart([_[1] for _ in cartResult.items()])
        freqLst=jFreq.getFreq([_[1] for _ in cartResult.items()])
        plt=jFreq.getFreqChart(freq=freqLst, title=title[subject])
        plt.savefig('%s\%s.png' % (self.TEMP_HOME, subject))
        chart[subject]='<img src="%s.png" width="800" height="600" />' % subject

        content=dict()
        subject='advert'
        content[subject]='<table style="border-style:none"><tr><td style="border-style:none;text-align:left;vertical-align:top">%s</td><td style="border-style:none;text-align:left;vertical-align:top">%s</td></tr></table>' % (table[subject], chart[subject])
        
        contents=[]
        for subject in subjects:
            contents.append([title[subject], desc[subject], subject])
            
        pages=[]        
        pages.append(lChm.getChapterHead(name='classify', title='Classifications', fileName='classify', parentName='cover', TEMP_HOME=self.TEMP_HOME, contents=contents))
        for page in subjects:
            p=lChm.getTemplate1(name=page, title=title[page], desc=desc[page], fileName=page, parentName='classify', TEMP_HOME=self.TEMP_HOME, content=content[page])
            pages.append(p)
        return pages


    def geneReportTa(self):
        import proj.lib.chart as jChart
        import proj.lib.chm as lChm
        import proj.hairycrab.twitter as hctw 
        import proj.lib.freq as jFreq
        
        subjects=['wordCount', 'tfidfText', 'tfidfClusterHeir', 'apriori']
        
        title=dict()
        title['wordCount']='Word Count'
        title['tfidfClusterHeir']='TF-IDF Hierachical Cluster'
        title['tfidfText']='TF-IDF Text Comparison'
        title['apriori']='Apriori'
        
        desc=dict()
        desc['wordCount']='Word Frequenct Count (Top 500)'
        desc['tfidfClusterHeir']='TFIDF Distance Hierachical Cluster Chart (100 samples)'
        desc['tfidfText']='Paired Text Samples, sorted by similarity, distinct user (100 samples)'
        desc['apriori']='Keywords association analysis using apriori algrithm'


        table=dict()
        table['wordCount']=jFreq.getFreqTable(freq=self.tweets.wc, count=500, noColumn=True)

        table['tfidfText']=self.tweets.TextAnalysis(100).getTopCloseTextTable(distinctUser=True, start=0, end=100)
        
        chart=dict()
        subject='wordCount'
        plt=jFreq.getFreqChart(freq=self.tweets.wc, title='Word Count')
        plt.savefig('%s\%s.png' % (self.TEMP_HOME, subject))
        chart[subject]='<img src="%s.png" width="800" height="600" />' % subject
       
        
        subject='tfidfClusterHeir'
        ta100=self.tweets.TextAnalysis(100)
        plt, ids=ta100.getChartHeirCluster()
        plt.savefig('%s\%s.png' % (self.TEMP_HOME, subject))
        chart[subject]='<img src="%s.png" width="800" height="600" />' % subject
        table[subject]=ta100.getChartHeirClusterTable(ids)
        
        content=dict()
        content['wordCount']='<table style="border-style:none"><tr><td style="border-style:none;text-align:left;vertical-align:top">%s</td><td style="border-style:none;text-align:left;vertical-align:top">%s</td></tr></table>' % (table['wordCount'], chart['wordCount'])
        content['tfidfClusterHeir']=chart['tfidfClusterHeir'] + '<br/>' + table['tfidfClusterHeir']
        content['tfidfText']=table['tfidfText']
        
        apriori_1=self.tweets.getApriori(minSupport=0.01, minConfinence=0.3, keywordList=['chromebook', 'touchscreen', 'aspire', 'laptop', 'computer', 'notebook', 'c720p', 'c720', 'touch'])
        apriori_2='<br/><div style="font-size:12pt">'
        for _ in apriori_1:
            apriori_2+='%s --> %s : %.2f%%<br/>' % (str(_[0]), str(_[1]), _[2]*100)
        apriori_2+='</div>'
        content['apriori']=apriori_2
        
        contents=[]
        for subject in subjects:
            contents.append([title[subject], desc[subject], subject])
        pages=[]        
        pages.append(lChm.getChapterHead(name='ta', title='Text Analysis', fileName='ta', parentName='cover', TEMP_HOME=self.TEMP_HOME, contents=contents))
        for page in subjects:
            p=lChm.getTemplate1(name=page, title=title[page], desc=desc[page], fileName=page, parentName='ta', TEMP_HOME=self.TEMP_HOME, content=content[page])
            pages.append(p)
        return pages

    def geneReportUsers(self, userIds=[]):
        import proj.lib.chart as jChart
        import proj.lib.chm as lChm
        import proj.hairycrab.twitter as hctw 
        import proj.lib.freq as jFreq

        userLst=self.tweets.getItem('raw.user.id')
        userIds=[_[0] for _ in jFreq.getFreq(userLst, proportion=True)][:20]
        #userIds=[1685288216, 178338718, 404375832, 379534850, 187094617, 1141069646, 57404155, 332305211, 767600131, 1553705328]
        
        subjects=userIds
        
        title=dict()
        for userId in subjects:
            title[userId]=str(userId)

        desc=dict()
        for userId in subjects:
            user=self.tweets.ss('raw.user.id', userId).getKVs('raw.user')[-1][1]
            desc[userId]='Tweets posted by %s(%s)' % (user['name'], str(userId))

        table=dict()
        for userId in subjects:
            tws=self.tweets.ss('raw.user.id', userId).getItems(['raw.id', 'stat.domains', 'raw.text'])
            t='<table><tr><th>Id</th><th>Url Domain</th><th>text</th></tr>'
            for tw in tws:
                try:
                    t+='<tr><td>%s</td><td>%s</td><td style="text-align:left">%s</td></tr>' % (str(tw[0]), ''.join([_+', ' for _ in tw[1]])[:-2], tw[2]) 
                except Exception:
                    t+=''
            t+=' </table>'
            table[userId]=t
        content=dict()
        for userId in subjects:
            content[userId]=table[userId]
            
        contents=[]
        for subject in subjects:
            contents.append([title[subject], desc[subject], subject])
        pages=[]        
        pages.append(lChm.getChapterHead(name='appendix', title='Appendix', fileName='appendix', parentName='cover', TEMP_HOME=self.TEMP_HOME, contents=[]))
        pages.append(lChm.getChapterHead(name='users', title='Users', fileName='users', parentName='appendix', TEMP_HOME=self.TEMP_HOME, contents=contents))
        for page in subjects:
            p=lChm.getTemplate1(name=page, title=title[page], desc=desc[page], fileName=str(page), parentName='users', TEMP_HOME=self.TEMP_HOME, content=content[page])
            pages.append(p)
        return pages        

