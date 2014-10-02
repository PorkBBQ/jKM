# -*- coding: utf-8 -*-
def getExcel(filePath):
    import xlrd
    return xlrd.open_workbook(filePath, encoding_override='big5')

def getMongodb(db='default'):
    import pymongo
    client=pymongo.MongoClient()
    return client[db]

def getUrl(url):
    import urllib2
    return urllib2.urlopen(url).read()

def getHBase(host='192.168.1.113', port='8070', user='bidamin', password='password'):
    import starbase
    connection=starbase.Connection(host, port, user, password)
    return connection

def getHive(host='192.168.220.150', port=10000):
    import hiver
    client=hiver.connect(host, port)
    return client

'''
import proj.jData as jData
hive=jData.getHive()
hive.execute('show tables')
hive.fetchAll()
'''


def getMySQL(host='10.24.100.136', user='root', db='josh_movieLens'):
    import MySQLdb  
    conn=MySQLdb.connect(host=host, user=user, db=db, charset="utf8")  
    return conn.cursor()   
    
    
def mongo2txt(db, coll, filePath):
    import proj.jData as jData    
    import json
    f = file(filePath, 'w')
    mongo=jData.getMongodb(db)
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

