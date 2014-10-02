
class Yahoo:
    def instance(self):
        print('''
import proj.hairycrab.yahoo as yahoo
reload(yahoo)
yh=yahoo.Yahoo()

stocks=yh.getStock(codeList=['2498.TW', 'AAPL', '005935.KS'])

import proj.jData as jData
mongo=jData.getMongodb('temp')
mongo['yahooStock'].drop()
for k,v in stocks.iteritems():
    mongo['yahooStock'].insert({k:v})

print(mongo['yahooStock'].count())
''')

    def getStock2HBase(self, dateStart='2013/1/1', dateEnd='2013/1/31', codeList=['']):
        import pandas as pd
        import pandas.io.data as web
        import proj.jData as jData
        codeFilePath=r'proj/hairycrab/yahoo/stockCodes.xlsx'
        mongo=jData.getMongodb('social')
        #mongo['yahooStock'].drop()
        #dateStart=dt.date(2003,1,1)
        #dateEnd=dt.date(2013,1,1)
        missingCodes=list()
        if len(codeList)==0:
            stockCodes=pd.ExcelFile(codeFilePath).parse('sheet1')
            codes=[str(a)+'.TW' for a in stockCodes['Code']]    
        else :
            codes=codeList
        #stockcodes=['AAPL', '2498.TW', '005935.KS']
        codes.sort()
        
        for code in codes:
            print('--> ' + code)
            try:
                df=web.get_data_yahoo(code, dateStart, dateEnd)
            except:
                print('!!! ' + code + ' not found !!!')
            #df=web.get_data_yahoo('0015.TW', '2013/1/1', '2013/1/31')
            if(type(df).__name__=='DataFrame'):
                data=list()
                for idx,row in df.iterrows():
                    daily=dict()
                    daily['date']=idx
                    for col in row.keys():
                        daily[col]=round(row[col], 2)
                    data.append(daily)
                    
                #result[code.replace('.', '@')]=data
                missingCodes.append(code.replace('.', '@'))
                mongo['yahooStock'].insert({'name':code.replace('.', '@'), 'data':data})
        #return result
        return missingCodes


        
    def getStock2Mongo(self, dateStart='2013/1/1', dateEnd='2013/1/31', codeList=[''], dbName='social', collectionName='yahooStock'):
        import pandas as pd
        import pandas.io.data as web
        import proj.jData as jData
        codeFilePath=r'proj/hairycrab/yahoo/stockCodes.xlsx'
        mongo=jData.getMongodb(dbName)
        #mongo['yahooStock'].drop()
        #dateStart=dt.date(2003,1,1)
        #dateEnd=dt.date(2013,1,1)
        missingCodes=list()
        if len(codeList)==0:
            stockCodes=pd.ExcelFile(codeFilePath).parse('sheet1')
            codes=[str(a)+'.TW' for a in stockCodes['Code']]    
        else :
            codes=codeList
        #stockcodes=['AAPL', '2498.TW', '005935.KS']
        codes.sort()
        for code in codes:
            print('--> ' + code)
            try:
                df=web.get_data_yahoo(code, dateStart, dateEnd)
            except:
                print('!!! ' + code + ' not found !!!')
            #df=web.get_data_yahoo('0015.TW', '2013/1/1', '2013/1/31')
            if(type(df).__name__=='DataFrame'):
                data=list()
                for idx,row in df.iterrows():
                    daily=dict()
                    daily['date']=idx
                    for col in row.keys():
                        daily[col]=round(row[col], 2)
                    data.append(daily)
                    
                #result[code.replace('.', '@')]=data
                missingCodes.append(code.replace('.', '@'))
                mongo[collectionName].insert({'name':code.replace('.', '@'), 'data':data})
        #return result
        return missingCodes
