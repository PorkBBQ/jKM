#!/home/biadmin/anaconda/bin/python

import json
import sys
import collections
import dateutil.parser as dp

digits=[str(_) for _ in range(1,101)]

def getReplaceList():
    replaceList=[]
    replaceList.append(['""', '"'])
    replaceList.append(['"craetedAt":', '"createdAt":'])
    replaceList.append(['"created_at":', '"createdAt":'])
    replaceList.append(['"session_id":', '"sessionID":'])
    replaceList.append(['"user_agent":', '"userAgent":'])
    replaceList.append(['"item_id":', '"itemId":'])
    return replaceList

def getDrillPaths():
    return {
        '/auth':0
        , '/createdAt':0
        , '/payload':1
        , '/refId':0
        , '/sessionID':0
        , '/type':1
        , '/user':0
        , '/userAgent':0
        , '/payload/itemId':0
        , '/payload/marker':0
        , '/payload/popular':1
        , '/payload/recent':0
        , '/payload/recommended':1
        , '/payload/recs/':1
        , '/payload/results':1
    }

def getSummaryTypes():    
    return {
        '/auth':'3'
        , '/createdAt':'date'
        , '/payload':'1'
        , '/refId':'3'
        , '/sessionID':'3'
        , '/type':'3'
        , '/user':'num'
        , '/userAgent':'1'
        , '/payload/itemId':'num'
        , '/payload/lengtg':'num'
        , '/payload/marker':'num'
        , '/payload/new':'freq10'
        , '/payload/old':'freq10'
        , '/payload/popular':'1'
        , '/payload/popular/':'freq10'
        , '/payload/rating':'freq10'
        , '/payload/recent':'3'
        , '/payload/recs':'3'
        , '/payload/recs/':'freq10'
        , '/payload/recommended':'3'
        , '/payload/recommended/':'freq10'
        , '/payload/results':'1'
        , '/payload/results/':'freq10'
    }   

def expand(item, path='', group='/'):
    drillPaths=getDrillPaths()
    if type(item) is dict:
        for k, v in item.items():
            p=path + '/' + str(k)
            t='dict'
            mapOut(p, str(v), t, g=group)
            d=drillPaths[p] if p in drillPaths else False
            if d: 
                expand(v, p, group=group)
                
    elif type(item) is list:
        for _ in item:
            p=path+'/'
            t='list'
            mapOut(p, str(_), t, g=group)
            d=drillPaths[p] if p in drillPaths else False
            if d: 
                expand(v, p, group=group)
    else:
        p=path+'/'+str(item)
        t=str(type(item)).replace("<type '", "").replace("'>", "")
        mapOut(p, str(item), t, g=group)


def mapOut(k, v='', t='', s='', g='/'):
    pathTypes=getSummaryTypes()
    if t in ['dict', 'list']:
        s='3'
    if k in pathTypes:
        s=pathTypes[k]
    out=k + '\t' + str(v) + '\t' + t + '\t' + str(s) + '\t' + g
    if env=='local':
        intermediate.append(out)
    elif env=='mr':
        print(out)

def mapper(env):

    it=open(inputFile).readlines() if env=='local' else sys.stdin

    for _ in it:
        _ = _.strip()
        for r1, r2 in getReplaceList():
            _ = _.replace(r1, r2)
        j=json.loads(_)

        if 'createdAt' in j:
            createdAt=dp.parse(j['createdAt']).strftime('%Y/%m/%d')
            try:
                createdAt=dp.parse(j['createdAt']).strftime('%Y/%m/%d')
            except ValueError:
                createdAt='_err: '
        else:
            createdAt=''
            
        if 'auth' in j:
            auth=j['auth']
        else:
            auth=''
            
        payload_itemId=''
        payload_length=''
        payload_marker=''
        payload_new=''
        payload_old=''
        payload_popular=[]
        payload_rating=[]
        payload_recent=''
        payload_recommended=[]
        payload_recs=[]
        payload_results=[]
        payload_subAction=''
        
        if 'payload' in j:
            pl=j['payload']
            if 'itemId' in pl: payload_itemId=pl['itemId']
            if 'length' in pl: payload_length=pl['length']
            if 'marker' in pl: payload_marker=pl['marker']
            if 'new' in pl: payload_new=pl['new']                
            if 'old' in pl: payload_old=pl['old']            
            
        out=''.join([j['auth']
            , '\t', createdAt
            , '\t', payload_itemId
            , '\t', payload_length
            , '\t', str(payload_marker)
            , '\t', payload_new
            , '\t', payload_old
            ])
        if env=='local':
            intermediate.append(out)
        elif env=='mr':
            print(out)
                
def reducer(env='local'):
    it=intermediate if env=='local' else sys.stdin
    for _ in it:
        print(_)


env='local' if len(sys.argv)==1 else 'mr'

if env=='local':
    inputFile=r'D:\Josh\data\DSC01\heckle\web.log.2'
    intermediate=[]
    mapper('local')
    reducer('local')
elif env=='mr':
    if sys.argv[1]=='-m':
        mapper('mr')
    elif sys.argv[1]=='-r':
        reducer('mr')
    
'''

hadoop fs -rmr /tmp/dsc01_02d

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_01d' \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_02d \
-file /home/biadmin/josh/script/dsc01/dsc01_02d.py \
-mapper "/home/biadmin/josh/script/dsc01/dsc01_02d.py -m" \
-reducer "uniq -c"

-reducer "/home/biadmin/josh/script/dsc01/dsc01_02d.py -r"

'''

'''
a='2013-05-06T08:00:08Z'
b='2013-05-12T23:06:11-08:00'

import dateutil

dateutil.parser.parse(a).strftime('%Y/%m/%d')
dateutil.parser.parse(b).strftime('%Y/%m/%d')
'''

'''

hadoop fs -rmr /tmp/dsc01_o1_01

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_o1_01' \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_o1_01 \
-file /home/biadmin/josh/dsc01_script/exploring/summary_map.py \
-file /home/biadmin/josh/dsc01_script/exploring/summary_reduce.py \
-mapper /home/biadmin/josh/dsc01_script/exploring/summary_map.py \
-reducer /home/biadmin/josh/dsc01_script/exploring/summary_reduce.py




hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_o1_01' \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_o1_01 \
-file /home/biadmin/josh/dsc01_script/exploring/summary_map_edit2.py \
-mapper /home/biadmin/josh/dsc01_script/exploring/summary_map_edit2.py \
-reducer "uniq -c"


hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_o1_04' \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_o1_04 \
-file /home/biadmin/josh/dsc01_script/exploring/summary_map_edit4.py \
-mapper /home/biadmin/josh/dsc01_script/exploring/summary_map_edit4.py \
-file /home/biadmin/josh/dsc01_script/exploring/summary_reduce.py \
-reducer /home/biadmin/josh/dsc01_script/exploring/summary_reduce.py


hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_o2_02' \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_o2_02 \
-file /home/biadmin/josh/dsc01_script/cleaning/clean_map_edit1.py \
-mapper /home/biadmin/josh/dsc01_script/cleaning/clean_map_edit1.py \
-file /home/biadmin/josh/dsc01_script/cleaning/clean_reduce.py \
-reducer /home/biadmin/josh/dsc01_script/cleaning/clean_reduce.py



hadoop fs -rmr /tmp/dsc01_o3_01

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_o3_01' \
-input /tmp/dsc01_o2_02 \
-output /tmp/dsc01_o3_01a \
-file /home/biadmin/josh/dsc01_script/classification/kid_map.py \
-mapper /home/biadmin/josh/dsc01_script/classification/kid_map.py \
-file /home/biadmin/josh/dsc01_script/classification/kid_reduce.py \
-reducer /home/biadmin/josh/dsc01_script/classification/kid_reduce.py


hadoop fs -cat /tmp/dsc01_o3_01/part-\* | cut -f1 | grep a > /tmp/adults
tail -n +21 /tmp/adults | hadoop fs -put - /tmp/dsc01_o3_01/adults_train
head -20 /tmp/adults | hadoop fs -put - /tmp/dsc01_o3_01/adults_test

hadoop fs -cat /tmp/dsc01_o3_01/part-\* | cut -f1 | grep k > /tmp/dsc01_o3_01/kids
tail -n +25 /tmp/kids | hadoop fs -put - /tmp/dsc01_o3_01/kids_train
head -24 /tmp/kids | hadoop fs -put - /tmp/dsc01_o3_01/kids_test


hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_o3_02' \
-input /tmp/dsc01_o3_01/part-00000 \
-output /tmp/dsc01_o3_02 \
-file /home/biadmin/josh/dsc01_script/classification/item_map.py \
-mapper /home/biadmin/josh/dsc01_script/classification/item_map.py \
-file /home/biadmin/josh/dsc01_script/classification/item_reduce.py \
-reducer /home/biadmin/josh/dsc01_script/classification/item_reduce.py

'''

'''
create table mydata (c1 string, c2 string, c3 int)
row format delimited
fields terminated by ','
;

load data inpath '/dir1/mydata'
overwrite into table mydata
;

'''

'''
s="/tmp/dsc01_o3_01/adults_train"
n=`hadoop fs -cat $s | wc -l | awk '{print $1}'`
e=`python -c "print(1.0/$n)"`
u=`id -u -n`

for line in `hadoop fs -cat $s`
do 
    echo -e "$line\t$e" >> v
done

hadoop fs -put v /tmp/dsc01_o3_01

hadoop fs -cat /tmp/dsc01_o3_01/part-00000
hadoop fs -cat /tmp/dsc01_o3_02/part-00000

hadoop fs -rmr /tmp/dsc01_o3_03

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-files /home/biadmin/v \
-files /home/biadmin/josh/dsc01_script/classification/simrank_map.py \
-mapper "/home/biadmin/josh/dsc01_script/classification/simrank_map.py v" \
-input /tmp/dsc01_o3_01/part-00000 \
-input /tmp/dsc01_o3_02/part-00000 \
-output /tmp/dsc01_o3_03

'''

'''
hadoop fs -rmr /tmp/dsc01/03/kid

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_03_kid' \
-input /tmp/dsc01_o2_02 \
-output /tmp/dsc01/03/kid \
-file /home/biadmin/josh/dsc01_script/classification/kid_map.py \
-mapper /home/biadmin/josh/dsc01_script/classification/kid_map.py \
-file /home/biadmin/josh/dsc01_script/classification/kid_reduce.py \
-reducer /home/biadmin/josh/dsc01_script/classification/kid_reduce.py

hadoop fs -cat /tmp/dsc01/03/kid/part-\* | cut -f1 | grep a > /tmp/adults
tail -n +21 /tmp/adults | hadoop fs -put - /tmp/dsc01/03/adults_train
head -20 /tmp/adults | hadoop fs -put - /tmp/dsc01/03/adults_test

hadoop fs -cat /tmp/dsc01/03/part-\* | cut -f1 | grep k > /tmp/kids
tail -n +25 /tmp/kids | hadoop fs -put - /tmp/dsc01/03/kids_train
head -24 /tmp/kids | hadoop fs -put - /tmp/dsc01/03/kids_test

n=`hadoop fs -cat /tmp/dsc01/03/adults_train | wc -l | awk '{print $1}'` 
e=`python -c "print(1.0/$n)"`
rm v
for line in `hadoop fs -cat /tmp/dsc01/03/adults_train`
do 
    echo -e "$line,\t$e" >> v
done


hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_03_item' \
-input /tmp/dsc01/03/kid/part-00000 \
-output /tmp/dsc01/03/item \
-file /home/biadmin/josh/dsc01_script/classification/item_map.py \
-mapper /home/biadmin/josh/dsc01_script/classification/item_map.py \
-file /home/biadmin/josh/dsc01_script/classification/item_reduce.py \
-reducer /home/biadmin/josh/dsc01_script/classification/item_reduce.py


hadoop jar $HADOOP_STREAMING \
-D mapred.job.name='dsc01_01' \
-input /user/root/data/dsc01/heckle \
-input /user/root/data/dsc01/jeckle \
-output /tmp/dsc01/01/01 \
-file /root/script/dsc01/exploring/summary_map.py \
-file /root/script/dsc01/exploring/summary_reduce.py \
-mapper /root/script/dsc01/exploring/summary_map.py \
-reducer /root/script/dsc01/exploring/summary_reduce.py


hadoop jar $HADOOP_STREAMING \
-input /user/root/data/dsc01/heckle/web.log.2 \
-output /tmp/t1 \
-mapper cat \
-reducer "uniq -c"

'''
