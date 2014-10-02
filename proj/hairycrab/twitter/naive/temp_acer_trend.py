
import json
from TwitterSearch import *
import pymongo

tokenId=2

if tokenId==1:
    consumer_key = 'n6Gbgdgwjpefdv0jLi2Fsg'
    consumer_secret = 'p6HmMy5H5gpRcfBIGrSoL9nkSCulJSxuMFb3feZ8xE'
    access_token = '1969088580-B9In02n5cUegsgDJHpOj8ONzTSQy10obf2tSWYU'
    access_token_secret = '8HdzpZlDlKEjNcEjAfx9s9Uyh3DjhMb2aaLJTKY2PQmqR'
    
if tokenId==2:
    consumer_key='lDL0CTZYMR2lexQfLWasiw'
    consumer_secret = 'KiUA9KNnS5OUVaJWZ0tchSOuVXkf26bBQJaBotNM'
    access_token = '2159968405-BUEOjBlDR9zIyyHr3nlOLVw8CWc86XoRvwiowFI'
    access_token_secret = 'Nw02kGDvJ7C0UBgGzWgymh1n2Ct9xmczAu5rM8XlqepYO'


brands=['acer', 'asus', 'lenovo', 'hp', 'dell']
keyWord=['acer OR asus OR lenovo OR hp OR dell']
#keyWord=['travelmate OR aspire']
pageSize=10
IncludeEntities=False
languageCode='en'

try:
    tso=TwitterSearchOrder()
    tso.setKeywords(keyWord)
    
    tso.setLanguage(languageCode)
    tso.setCount(pageSize)
    tso.setIncludeEntities(IncludeEntities)
#    tso.setUntil(datetime.date(2013, 10, 24))

    ts = TwitterSearch(
        consumer_key = consumer_key
        , consumer_secret = consumer_secret
        , access_token = access_token
        , access_token_secret = access_token_secret
     )
     
    t= ts.searchTweetsIterable(tso)

    tweets=[]
    cnt=0

    for tweet in ts.searchTweetsIterable(tso): # this is where the fun actually starts :)
        #print(tweet)        
        tweets.append(tweet)
        cnt+=1
        if cnt>=5:
            exit

    print(len(tweets))
    

    cnts=[0, 0, 0, 0, 0]
    for tweet in tweets:
        for i in range(len(brands)):
            if brands[i] in tweet['text'].lower():
                cnts[i]+=1
    print(cnts)
    
    
#    json.dumps(tweets[0], indent=4)
#    tweets[0]['text']
        #print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)

#==========================================================

print(len(tweets))

client=pymongo.MongoClient()
mongotw=client['social']['twitter']

for tweet in tweets:
    mongotw.insert(tweet)
print(mongotw.count())
