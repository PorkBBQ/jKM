'''
    version=0.2
'''

class KM:
    import excel
    import mongodb
    import chm
    import html
    import html_rows
    
    def __init__(self, KM_HOME=r'C:\Dropbox\Python\proj\jKM'):
        self.env=dict()
        self.env['KM_HOME']=KM_HOME
        self.env['KM_DATA']=self.env['KM_HOME'].join(r'\data')        
        self.env['KM_TEMP']=self.env['KM_HOME'].join(r'\temp')
        self.env['outputPaths']=[self.env['KM_HOME'] + r'\report', r'C:\Dropbox\ACER_DB2\Josh']
        
    def update_All(self):
        #mongo update_all
        import proj.jKM as jKM        

        km=jKM.KM()
        
        #collections=km.excel.getCollections()
        #km.mongodb.update(subjects)
        
        #-- generate Chm ---
        collection=km.excel.getCollection()
        km.chm.generateHtmls(collection)
        km.chm.generateChm(collection, self.KM_TEMP)
        
    def help(self):
        print(r'''
import proj.jKM
reload(proj.jKM)
km=proj.jKM.KM()

env={
    'name':'km'
    , 'KM_HOME':r'C:\Dropbox\Python\proj\jKM'
    , 'KM_DATA':r'C:\Dropbox\Python\proj\jKM\data'
    , 'KM_TEMP':r'C:\Dropbox\Python\proj\jKM\temp'
    , 'outputPaths':[r'C:\Dropbox\Python\proj\jKM\report']
}
    
collection=km.excel.getCollection(env)
km.chm.generateHtmls(env, collection)
km.chm.generateChm(env, collection)
    ''')
        
    def instance(self):
        instance='''

#=Update All====================================
import proj.jKM as jKM
km=jKM.KM()
km.update_All()

#===============================================

#mongo check
mongo=jData.getMongodb('KM')
mongo['KM'].count()
km.mongodb.getNames()

#mongo update one file
excel=jData.getExcel(km.KM_HOME+'\\hadoop.xlsx')
subjects=km.excel.getSubject(excel, 'hadoop')
print('\n')
[doc['name'] for doc in subjects['docs']]
print('\n')
km.mongodb.update([subjects])

#mongo drop
mongo=jData.getMongodb('KM')
mongo['KM'].drop()
km.mongodb.getNames()

        '''
        print(instance)