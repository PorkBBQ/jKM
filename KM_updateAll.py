# -*- coding: utf-8 -*-

import proj.jKM
import json

reload(proj.jKM)

env={}
env['NAME']='Encyclopedia'
env['KM_HOME']=r'C:\Dropbox\Python\proj\jKM'
env['KM_DATA']=env['KM_HOME'] + r'\data'
env['KM_TEMP']=env['KM_HOME'] + r'\temp'
env['OUTPUTS']=r'C:\Dropbox\Python\proj\jKM\report,C:\josh\docs\km'
env['ENABLE_CATEGORY']=False
#env['BOOKS']=['BigInsights.xlsx']


book=proj.jKM.excel.getBook(env)
proj.jKM.html.generateHtmls(env, book)
#proj.jKM.html_rows.generateHtmls(env, collection)

proj.jKM.chm.generateChm(env, book)
#proj.jKM.mongodb.put(book)

