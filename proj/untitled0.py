# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 14:59:11 2014

@author: Josh
"""

import xlrd
w=xlrd.open_workbook(r'C:\Dropbox\Python\proj\jKM\data\CDH_121.xlsx')
s=w.sheet_by_name('l_Impala')
c2=s.cell_value(38,3)
print(''.join(['<html>', c2.encode('cp950')]))

import proj.jHtml as jHtml
jHtml.Tag(tagType='p', innerHtml=c2)
html=jHtml.Html()
html.addTag(jHtml.Tag(tagType='p', innerHtml=c2))

print(html.getHtml())
html.save(r'a.html')


import proj.jKM
reload(proj.jKM)
km=proj.jKM.KM()
km.help()

env={
    'name':'km'
    , 'KM_HOME':r'C:\Dropbox\Python\proj\jKM'
    , 'KM_DATA':r'C:\Dropbox\Python\proj\jKM\data'
    , 'KM_TEMP':r'C:\Dropbox\Python\proj\jKM\temp'
    , 'outputPaths':[r'C:\Dropbox\Python\proj\jKM\report']
}
    
collection=km.excel.getCollection(env)
#km.chm.generateHtmls(env, collection)
#km.chm.generateChm(env, collection)

t=collection['BigInsights']['HBase Rest Port'][11]['remark']
html.addTag(jHtml.Tag(tagType='p', innerHtml=t))
html.save(r'a.html')
