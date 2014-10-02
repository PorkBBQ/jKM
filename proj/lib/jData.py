# -*- coding: utf-8 -*-

def getExcel(filePath):
    import xlrd
    return xlrd.open_workbook(filePath)

def getMongodb(db):
    import pymongo
    client=pymongo.MongoClient()
    return client[db]

def getWebPage(url, code='big5'):
    import urllib2
    content=urllib2.urlopen(url).read()
    return content.decode('utf-8').encode('big5', 'ignore')
    
def getHbase(host='192.168.1.125', port='8070', user='bidamin', password='password'):
    import starbase
    connection=starbase.Connection(host, port, user, password)
    return connection

def insertHbaseOne(hbase, dct={'r1':'v1'}, tableName='test', columnName='cf1:c1'):
    import time, json
    time1=time.time()

    table=hbase.table(tableName)
    batch=table.batch()
    for k, v in dct.items():
        columns={columnName:json.dumps(v)}
        #print((str(k), columns))
        batch.insert(str(k), columns)
    batch.commit(finalize=True)
    print("%d rows --> HBase(%s):'%s', in %.2f seconds" % (len(dct), hbase.host, tableName, time.time()-time1))


def insertHbase(hbase, tableName='test', cfName='test', dct={'r1':'v1'}):
    import time, json
    time1=time.time()

    table=hbase.table(tableName)
    batch=table.batch()
    #table.insert('409310373997981696', {'anno:anno1': 'v_a1', 'anno:anno2': 'v_a2', 'anno:anno3': 'v_a3'})
    for k, v in dct.items():
        columns={}
        for vk, vv in v.items():
            columnName=cfName+':'+str(vk)
            columns[columnName]=json.dumps(vv)
        #print((str(k), columns))
        batch.insert(str(k), columns)
    batch.commit(finalize=True)
    print("%d rows --> HBase(%s):%s.%s, in %.2f seconds" % (len(dct), hbase.host, tableName, cfName, time.time()-time1))
    
def mongo2txt(db, coll, filePath):
    import json
    f = file(filePath, 'w')
    mongo=getMongodb(db)
    for r in mongo[coll].find({}, {'_id':0}):
       f.write(json.dumps(r, indent=2).encode('utf-8'))
       f.write('\n')
    f.close()
    print('export ' + db + '.' + coll + ' --> ' + filePath)
    
def writeFile(fileName, str):
    f = file(fileName,'w')
    f.write(str)
    f.close()

def writeRemoteFile(host, fileName, str, port=22, username='root', password='password'):
    import ssh
    client = ssh.SSHClient()
    client.set_missing_host_key_policy(ssh.AutoAddPolicy())
    client.connect(host, port=port, username=username, password=password)
    stdin, stdout, stderr = client.exec_command('echo ' + str + ' >> ' + fileName)


