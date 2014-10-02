# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 14:46:25 2013

@author: 1309075
"""

class TextAnalysis:
    def __init__(self, tweets, maxCount=-1):
        if maxCount==-1:
            maxCount=tweets.getCount()
        a1=tweets.getSubDct('raw.text')
        self.dctText={}
        for k, v in a1.items()[100:100+maxCount]:
            self.dctText[k]=v
        self.tweets=tweets

    def getTf(self):
        import proj.lib.textAnalysis as ta
        return ta.tf(self.dctText)

    def getIdf(self):
        import proj.lib.textAnalysis as ta
        return ta.idf(self.dctText)

    def getTfidf(self):        
        import proj.lib.textAnalysis as ta
        return ta.tfidf(self.dctText)
        
    def getCosSimMatrix(self):
        import proj.lib.textAnalysis as ta
        return ta.cosSimMatrix(ta.tfidf(self.dctText))
        
    def getTopCloseText(self, distinctUser=False, start=0, end=10):
        temp1=self.getCosSimMatrix()
        temp2=[_ for _ in temp1.items() if _[0][0]!=_[0][1]]
        temp3=[[v, k[0], k[1]] for k, v in temp2 if k[0]<k[1]]
        temp3.sort()
        temp4=[
                {'distance':_[0]
                , 'tweetId_1':_[1]
                , 'tweetId_2':_[2]
                , 'text_1':self.tweets.docs[_[1]]['raw']['text']
                , 'text_2': self.tweets.docs[_[2]]['raw']['text']
                , 'userId_1': self.tweets.docs[_[1]]['raw']['user']['id']
                , 'userId_2': self.tweets.docs[_[2]]['raw']['user']['id']
                , 'userName_1': self.tweets.docs[_[1]]['raw']['user']['name']
                , 'userName_2': self.tweets.docs[_[2]]['raw']['user']['name']
                } for _ in temp3]
        if distinctUser==True:
            temp4=[_ for _ in temp4 if _['userId_1']!=_['userId_2'] and _['userName_1']!=_['userName_2']]
        temp5=temp4[start:end]
        return temp5
    
    def getTopCloseTextTable(self, distinctUser=False, start=0, end=10):    
        a=self.getTopCloseText(distinctUser=distinctUser, start=start, end=end)
        tables=''        
        for _ in a:
            table='<table width="90%%">'
            table+='<tr><td>Distance</td><td style="text-align:left" colspan="2">%.4f</td></tr>' % (_['distance'])
            table+='<tr><td width="10%%">Id</td><td width="45%%">%s</td width="45%%"><td>%s</td></tr>' % (str(_['tweetId_1']), str(_['tweetId_2']))
            table+='<tr><td>User</td><td>%s (%s)</td><td>%s (%s)</td></tr>' % (_['userName_1'].encode('utf8', 'ignore').decode('ascii', 'ignore'), str(_['userId_1']),_['userName_2'].encode('utf8', 'ignore').decode('ascii', 'ignore'), str(_['userId_2']))
            table+='<tr><td>Text 1</td><td style="text-align:left" colspan="2">%s</td></tr>' % _['text_1'].encode('utf8', 'ignore').decode('ascii', 'ignore')
            table+='<tr><td>Text 2</td><td style="text-align:left" colspan="2">%s</td></tr>' % _['text_2'].encode('utf8', 'ignore').decode('ascii', 'ignore')
            table+='</table><br/>'
            tables+=table
        return tables
        
    def showTopCloseText(self, distinctUser=False, start=0, end=10):    
        a=self.getTopCloseText(distinctUser=distinctUser, start=start, end=end)
        for _ in a:
            try:
                print('distance: %.4f between (%s,%s)' % (_['distance'], str(_['tweetId_1']), str(_['tweetId_2'])))
                print('user_1: %s(%d),  user_2: %s(%d)' % (_['userName_1'], _['userId_1'], _['userName_2'], _['userId_2']))
                print('--> text_1: %s' % _['text_1'])
                print('--> text_2: %s' % _['text_2'])
                print('')
            except Exception:
                print('UnicodeException!')
                print('')
        return ''
        
    def getChartHeirCluster(self):
        import proj.lib.textAnalysis as ta        
        return ta.getHieChart(self.dctText)
        

    def getChartHeirClusterTable(self, ids):
        table='<table></tr><th>No</th><th>Tweet Id</th><th>User</th><th>Text</th></tr>'
        for _ in ids:
            table+='<tr><td>%d</td><td>%s</td><td>%s(%d)</td><td style="text-align:left">%s</td></tr>' % (_[0], str(_[1]), self.tweets.docs[_[1]]['raw']['user']['name'], self.tweets.docs[_[1]]['raw']['user']['id'], self.tweets.docs[_[1]]['raw']['text'])
        return table
        
        
        
        