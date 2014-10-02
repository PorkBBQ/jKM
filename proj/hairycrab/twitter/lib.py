# -*- coding: utf-8 -*-

def created_at2datetime(created_at):
    import datetime
    return datetime.datetime.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y')

def created_HbaseTable(hbase, tableName, dropIfExist=False):
    import proj.lib.jData as jData
    #hbase=jData.getHbase('192.168.1.125')
    table=hbase.table(tableName)
    if dropIfExist:
        if table.exists():
            print("===  drop hbase(%s) table: '%s'  ===" %(hbase.host, tableName))
            table.drop()
    
    print("===  create hbase(%s) table: '%s'('meta', 'raw', 'stat', 'anno')  ===" %(hbase.host, tableName))
    table.create('meta', 'raw', 'stat', 'anno')
    
def loadTweets(hbase='_default', tableName='test'):
    import proj.lib.jData as jData
    import proj.hairycrab.twitter as hctw
    import time, json
    
    if hbase=='_default':
        hbase=jData.getHbase()
        
    time1=time.time()
    docs={}    
    table=hbase.table(tableName)
    
    for row in table.fetch_all_rows():
        _id=long(row['raw']['id'])
        doc={}
        for cf in ['meta', 'raw', 'stat', 'anno']:
            doc[cf]={}
            if cf in row:
                for c in row[cf]:
                    try:
                        doc[cf][c]=json.loads(row[cf][c])
                    except Exception:
                        doc[cf][c]=row[cf][c]
        docs[_id]=doc

    print("HBase(%s):'%s' --> %d tweets , in %.2f seconds" %(hbase.host, tableName, len(docs.keys()), time.time()-time1 ))
    return hctw.Tweets(docs=docs)

def downloadTweets(q
            , count=100
            , tokenNo=1
            , lang=''
            , max_id=999999999999999999999
            , result_type='mixed'
            , until=''
            #, until='2013-11-25'
            ):
    import twitter
    import tweets as tw
    raws=list()
    tweetsToGo=count

    if tokenNo==1:
        CONSUMER_KEY='lDL0CTZYMR2lexQfLWasiw'
        CONSUMER_SECRET='KiUA9KNnS5OUVaJWZ0tchSOuVXkf26bBQJaBotNM'
        oauth_token='2159968405-BUEOjBlDR9zIyyHr3nlOLVw8CWc86XoRvwiowFI'
        oauth_secret='Nw02kGDvJ7C0UBgGzWgymh1n2Ct9xmczAu5rM8XlqepYO'
    if tokenNo==2:
        CONSUMER_KEY='n6Gbgdgwjpefdv0jLi2Fsg'
        CONSUMER_SECRET='p6HmMy5H5gpRcfBIGrSoL9nkSCulJSxuMFb3feZ8xE'
        oauth_token='1969088580-B9In02n5cUegsgDJHpOj8ONzTSQy10obf2tSWYU'
        oauth_secret='8HdzpZlDlKEjNcEjAfx9s9Uyh3DjhMb2aaLJTKY2PQmqR'
    if tokenNo==3:
        CONSUMER_KEY='6FTXkTJE2CAk5PGF9CQfYw'
        CONSUMER_SECRET='6JD0zKEVsJAxhB6CfQp5GjfrJ72xgHnFAL0hjqbcY'
        oauth_token='1969088580-NYGUcgYmN0GPH5FYCfVQEiw7RCVUUe8tfQsNCsr'
        oauth_secret='WhpjmtViHuMbzbNwWZEu3rlKLSgeojJnaxAkwtOGmUaw7'
    if tokenNo==4:
        CONSUMER_KEY='NipEmhUizIrjbHLm4mCQ6g'
        CONSUMER_SECRET='LAwYeTnepX3solP4Zuw21HZZ24SyefK0puWezooEw4'
        oauth_token='1969088580-9awCrRaJ1JsQYap3yauZRxGgEWI0TJtns9fylJG'
        oauth_secret='s4UT3tI0BbY2ovI17C3jOTboccGDY9JIqbsZI8PVd7DEK'
    if tokenNo==5:
        CONSUMER_KEY='hrFtajNUaFj6FL4uyG48w'
        CONSUMER_SECRET='QLvLbfSZZgMCuqu9I5KiKxJaM2gIShQCPYrpBAJbs'
        oauth_token='1969088580-iNMlnby0n0goBVd7Z5ZxgMcfqO8xFNoE2cTljI1'
        oauth_secret='2I30SGIArcYtF2fqFzzq2tgFxnBFBpCelDBh5qwxILshM'
    if tokenNo==6:
        CONSUMER_KEY='7dR3ZjmaIhNAOZvXgjtGOw'
        CONSUMER_SECRET='kDalRjBvNNsZf9Fi9kcV7TdjRtAYHXbHPN2qJfDLBb4'
        oauth_token='1969088580-p23L4LPKTs5jaHZNXradKhnQA2giR8anHELoR5t'
        oauth_secret='FeQ9Rq8jo2EkdcnLAcxbZZySyPpMxy7jzQNuOPRt1yqFf'
    if tokenNo==7:
        CONSUMER_KEY='cAml5LjTW7NGxv2UqeLihQ'
        CONSUMER_SECRET='YCARJvJdTsfEVTLwPqwt76rs9UmkHJoKvJmnzxeOA'
        oauth_token='1969088580-0Z3qwtcL4y0SuiZM4Iff9yL6mPF9GqVL5xq46FS'
        oauth_secret='4r2lkoyxBAsrCrstnRDWMsNmHYVbmbDt053Y1LeifTkkj'
    if tokenNo==8:
        CONSUMER_KEY='F4FLwIAdCOTz2M9PGZGvg'
        CONSUMER_SECRET='Y49HWGYlBrqMMhLq00YLy5zCcyrAkWyS78gvCf78'
        oauth_token='1969088580-cIe4z2FRohEZjEYuFVHeoRpInSi8UFR9rsYCAH8'
        oauth_secret='LC30Peu3VvafmmgnCjmEGI6cr2J6wqKF9JsSMij4f7OvC'   
    if tokenNo==9:
        CONSUMER_KEY='nRH3IrgvyJOpHgzoLz5tiw'
        CONSUMER_SECRET='WncllQUed7inw82tCDzIFPR3lybqoGqNXGdFoYVmU'
        oauth_token='1969088580-7OhWbVOY24cQpLJpqh2rucztMzD4BBIqi6V8kpm'
        oauth_secret='RXGdhdtd1b0RgBJHiYHZd82X5eKwCgAxf9iPKYwrKEg1V'   
    if tokenNo==10:
        CONSUMER_KEY='MWvUQUsR8OrgLT3wWGq03g'
        CONSUMER_SECRET='YJBloJrwzoUXswI6tP9K9OzqJmyjKdXsIIdYRJJzibs'
        oauth_token='1969088580-83vE90jF6ZjuZBbi6Rg6BY8s91N5UCu9C2iyIMm'
        oauth_secret='zLsgVVx6i3LPbjAhhPwzB45qTe9VrajRmR7Y6mRJQmMpf'   

    t = twitter.Twitter(auth=twitter.OAuth(
        oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

    nex_max_id=max_id
    
    while tweetsToGo>0:
        print(str(tweetsToGo) + ' tweets to go ...')
        s=t.search.tweets(q=q
                        , count=count
                        , lang=lang
                        , max_id=int(nex_max_id)-1
                        , result_type=result_type
                        , until=until
                        )
        raws.extend(s['statuses'])
        tweetsToGo=tweetsToGo-int(s['search_metadata']['count'])
        if len(s['statuses'])>0:
            nex_max_id=s['statuses'][-1]['id_str']
        else:
            print('===== No more tweets! =====')
            return tw.Tweets(raws)
    print('--> %d tweets downloaded' % len(raws))
    return tw.Tweets(raws)
    #len(tweets)

# =============================================

def downloadBigTweets(q=['acer']
                , batchCount=1
                , token_offset=1
                , lang=''
                , max_id=999999999999999999999
                , result_type='mixed'
                , until=''
                ):
    import time
    import proj.hairycrab.twitter as hctw
    import proj.jData as jData
    next_max_id=99999999999999999999
    time1=time.time()
    allRaws=[]
    for i in range(batchCount):
        tws=downloadTweets(q, count=10000, tokenNo=i+token_offset, lang=lang, max_id=next_max_id, result_type=result_type, until=until)
        next_max_id=tws.getStats()['minId']
        allRaws.extend(tws.raws)
    tweets=hctw.Tweets(allRaws)
    print('--> %d tweets, in %.2f seconds'% (len(allRaws), time.time()-time1))
    return tweets    
    
def saveBigTweets(q=['acer'], host='192.168.220.150', port='8070', tableName='test', lang='en', token_offset=1, batchCount=1):
    import time
    import proj.hairycrab.twitter as hctw
    import proj.jData as jData
    next_max_id=99999999999999999999
    time1=time.time()
    for i in range(batchCount):
        raws=hctw.getTweets(q, count=10000, tokenNo=i+token_offset, lang=lang, max_id=next_max_id)
        raws.getCount()
        raws.getStats()
        hbase=jData.getHBase(host, port)
        raws.save2HBase(hbase, tableName, {}, False)
        next_max_id=raws.getMinId()
    print(time.time()-time1)
    
    