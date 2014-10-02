# -*- coding: utf-8 -*-
"""
Created on Fri Dec 06 14:04:41 2013

@author: 1309075
"""


def getDict(proj, name, DICT_HOME=r'proj\albatross\dict'):
    import proj.jData as jData
    excel=jData.getExcel(r'%s\%s.xlsx' %(DICT_HOME, proj))
    sheet=excel.sheet_by_name(name)
     
    dic=[]
    for i in range(sheet.nrows):
        dic.append(sheet.cell(i, 0).value)
    return dic