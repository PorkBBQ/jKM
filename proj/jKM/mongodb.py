import proj.jData as jData

def put(book, dbName='jKM', bookName='Notes'):
    #names=collection.keys()
    db=jData.getMongodb()
    #db.drop_collection(collectionName)
    coll=db[bookName]
    coll.insert(book)
    print('--> Mongodb  {db:%s, collection:%s}' %(dbName, bookName))
    
    
def get(dbName='jKM', collectionName='Notes'):
    db=jData.getMongodb()
    coll=db[collectionName]
    return coll.find()