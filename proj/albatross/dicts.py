# -*- coding: utf-8 -*-
"""
Created on Fri Dec 06 14:05:05 2013

@author: 1309075
"""

def getDict(proj, name, DICT_HOME=r'proj\albatross\excel'):
    import proj.jData as jData
    excel=jData.getExcel(r'%s\%s.xlsx' %(DICT_HOME, proj))
    sheet=excel.sheet_by_name(name)
     
    dct={}
    for i in range(1, sheet.nrows):
        k=sheet.cell(i, 0).value
        dct[k]={}
        for j in range(sheet.ncols):
            header=sheet.cell(0, j).value
            dct[k][header]=sheet.cell(i, j).value
    return dct